print("DEBUG: The script has started.")
import os
import glob
import faiss
import torch

from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
from rich.console import Console
from rich.prompt import Prompt

console = Console()

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LM_NAME = "microsoft/phi-2"

device = "cuda" if torch.cuda.is_available() else "cpu"


def load_embedding_model():
    console.print("[bold green]Loading embedding model...[/bold green]")
    model = SentenceTransformer(EMBED_MODEL_NAME, device=device)
    return model


def load_lm():
    console.print("[bold green]Loading language model...[/bold green]")
    tokenizer = AutoTokenizer.from_pretrained(LM_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        LM_NAME,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto"
    )
    return tokenizer, model


def load_documents(data_dir="data"):
    console.print(f"[bold blue]Loading documents from {data_dir}...[/bold blue]")
    docs = []
    paths = glob.glob(os.path.join(data_dir, "*.txt"))
    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append((os.path.basename(p), text))
    console.print(f"[bold blue]Loaded {len(docs)} documents.[/bold blue]")
    return docs


def build_index(docs, embed_model):
    console.print("[bold green]Building vector index...[/bold green]")
    texts = [d[1] for d in docs]
    embeddings = embed_model.encode(texts, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, embeddings


def retrieve(query, docs, embed_model, index, k=3):
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, k)
    results = []
    for idx in I[0]:
        if idx < 0 or idx >= len(docs):
            continue
        results.append(docs[idx])
    return results


def generate_business_answer(tokenizer, model, query, context):
    system_prompt = (
        "You are an elite business strategist and sales negotiator. "
        "You think like a senior VP with deep experience in B2B sales, "
        "pricing, risk analysis, and negotiation. "
        "Use the provided context from documents, but also apply strong reasoning. "
        "Be concrete, structured, and practical.\n\n"
    )

    context_text = ""
    for name, text in context:
        context_text += f"[DOCUMENT: {name}]\n{text[:2000]}\n\n"

    prompt = (
        system_prompt
        + "Context:\n"
        + context_text
        + "\n\nUser question:\n"
        + query
        + "\n\nAnswer with clear bullet points and a short action plan.\n"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
        )
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    if "User question:" in output:
        output = output.split("User question:")[-1]
        if "\n\n" in output:
            output = output.split("\n\n", 1)[-1]
    return output.strip()


def main():
    console.print("[bold magenta]Sovereign Negotiator – Offline Sales AI[/bold magenta]")

    embed_model = load_embedding_model()
    tokenizer, model = load_lm()
    docs = load_documents("data")

    if not docs:
        console.print(
            "[bold red]No documents found in ./data. "
            "Add some .txt files with contracts, proposals, emails, etc.[/bold red]"
        )

    index, _ = build_index(docs, embed_model) if docs else (None, None)

    while True:
        query = Prompt.ask("\n[bold yellow]Ask a negotiation/business question (or type 'exit')[/bold yellow]")
        if query.lower().strip() in ["exit", "quit"]:
            break

        if docs and index is not None:
            context = retrieve(query, docs, embed_model, index, k=3)
        else:
            context = []

        answer = generate_business_answer(tokenizer, model, query, context)
        console.print("\n[bold cyan]Sovereign Negotiator:[/bold cyan]")
        console.print(answer)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n--- AN ERROR OCCURRED ---")
        print(e)
        input("\nPress Enter to exit...")