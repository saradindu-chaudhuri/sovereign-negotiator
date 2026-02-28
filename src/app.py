import streamlit as st
import os
import glob
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set page config
st.set_page_config(page_title="Sovereign Negotiator", layout="centered")

# --- CORE LOGIC ---
@st.cache_resource
def load_resources():
    # Loading Phi-2 for local inference
    embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
    model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", device_map="auto")
    return embed_model, tokenizer, model

embed_model, tokenizer, model = load_resources()

# --- UI LAYER ---
st.title("💼 Sovereign Negotiator")
st.subheader("Your Offline AI Sales Copilot")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload a contract or deal document (.txt)", type=['txt'])
context_text = ""

if uploaded_file is not None:
    context_text = uploaded_file.read().decode("utf-8")
    st.success(f"Loaded: {uploaded_file.name}")
else:
    # Default fallback to /data folder
    paths = glob.glob(os.path.join("data", "*.txt"))
    if paths:
        with open(paths[0], "r", encoding="utf-8") as f:
            context_text = f.read()

# 2. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the negotiation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Construct Prompt
            full_prompt = f"Context: {context_text}\n\nQuestion: {prompt}\n\nAnswer:"
            inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
            
            output_ids = model.generate(**inputs, max_new_tokens=300)
            answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            # Clean up output
            final_answer = answer.split("Answer:")[-1].strip()
            st.markdown(final_answer)
            
    st.session_state.messages.append({"role": "assistant", "content": final_answer})