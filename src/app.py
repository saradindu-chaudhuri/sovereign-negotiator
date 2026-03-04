import streamlit as st
from groq import Groq
import datetime

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Sovereign Negotiator", layout="wide", page_icon="⚖️")

# ---------------------------------------------------------
# MODEL INIT
# ---------------------------------------------------------
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()
MODEL_NAME = "llama3-70b-8192"

# ---------------------------------------------------------
# PERSONAS
# ---------------------------------------------------------
STRATEGIES = {
    "💼 Corporate Attorney": "Formal, precise, authoritative. Focus on risk mitigation and ROI.",
    "🤝 Diplomatic Mediator": "Master mediator. Focus on de-escalation and ZOPA.",
    "💰 Salary Maximizer": "Compensation strategist. Data-driven, assertive, value-focused.",
    "🏗️ Procurement Expert": "Negotiate vendor contracts. Focus on leverage and concessions.",
    "🏢 Startup Founder": "Investor negotiations. Focus on storytelling and strategic framing."
}

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------
def ask_groq(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Sovereign Negotiator, an elite negotiation strategist. "
                    "Provide structured, practical, high‑leverage negotiation advice."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.sidebar.title("⚖️ Negotiation Suite")
selected_strategy = st.sidebar.selectbox("Select Expert Persona:", list(STRATEGIES.keys()))
st.title(f"Sovereign Negotiator: {selected_strategy}")

# ---------------------------------------------------------
# STRATEGY BUILDER
# ---------------------------------------------------------
with st.expander("🚀 Build your Strategy Plan"):
    scenario = st.text_area("Describe your situation (goal, opponent, leverage):")
    if st.button("Generate Strategic Blueprint"):
        if scenario.strip():
            with st.spinner("Analyzing leverage..."):
                prompt = (
                    f"Act as {selected_strategy}. "
                    f"{STRATEGIES[selected_strategy]}. "
                    f"Create a structured 3-step negotiation plan for: {scenario}"
                )
                answer = ask_groq(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.warning("Please describe your scenario first.")

# ---------------------------------------------------------
# CHAT
# ---------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask for a counter-argument or tactic..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = ask_groq(
        f"Persona: {selected_strategy}. User question: {user_input}"
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------------------------------------------------------
# EXPORT
# ---------------------------------------------------------
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("📥 Download Report", transcript, file_name="negotiation_report.txt")
