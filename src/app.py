import streamlit as st
import google.generativeai as genai
import datetime
import time

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Sovereign Negotiator", layout="wide", page_icon="⚖️")

# Use the current model standard
MODEL_NAME = "gemini-3-flash"

@st.cache_resource
def get_model():
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    return genai.GenerativeModel(MODEL_NAME)

# ---------------------------------------------------------
# STRATEGIES
# ---------------------------------------------------------
STRATEGIES = {
    "💼 Corporate Attorney": "Formal, precise, authoritative. Focus on risk mitigation and ROI.",
    "🤝 Diplomatic Mediator": "Master mediator. Focus on de-escalation and ZOPA.",
    "💰 Salary Maximizer": "Compensation strategist. Data-driven, assertive, value-focused.",
    "🏗️ Procurement Expert": "Negotiate vendor contracts. Focus on leverage and concessions.",
    "🏢 Startup Founder": "Investor negotiations. Focus on storytelling and strategic framing."
}

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.sidebar.title("⚖️ Negotiation Suite")
selected_strategy = st.sidebar.selectbox("Select Expert Persona:", list(STRATEGIES.keys()))
st.title(f"Sovereign Negotiator: {selected_strategy}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- APP LOGIC ---
model = get_model()

with st.expander("🚀 Build your Strategy Plan"):
    scenario = st.text_area("Describe your situation (goal, opponent, leverage):")
    if st.button("Generate Strategic Blueprint"):
        if scenario.strip():
            with st.spinner("Analyzing leverage..."):
                prompt = f"Act as {selected_strategy}. {STRATEGIES[selected_strategy]}. Create a 3-step action plan for: {scenario}"
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Negotiator is busy (Quota Limit). Please wait 30 seconds and try again.")
        else:
            st.warning("Please describe your scenario first.")

# --- CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask for a counter-argument or tactic..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        try:
            # We don't need 'chat' objects; generate_content is cleaner for this UI
            response = model.generate_content(f"Persona: {selected_strategy}. User: {user_input}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Negotiator is currently throttled. Please wait a moment.")

# --- EXPORT ---
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("📥 Download Report", transcript, file_name="negotiation_report.txt")