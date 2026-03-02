import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIG ---
st.set_page_config(page_title="Sovereign Negotiator", layout="wide", page_icon="⚖️")

# --- MODEL (Cached) ---
@st.cache_resource
def get_model():
    # Only run this once
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_model()

# --- PERSONAS ---
STRATEGIES = {
    "💼 Corporate Attorney": "Formal, precise, authoritative. Focus on risk mitigation and ROI.",
    "🤝 Diplomatic Mediator": "Master mediator. Focus on de-escalation and ZOPA.",
    "💰 Salary Maximizer": "Compensation strategist. Data-driven, assertive, value-focused.",
    "🏗️ Procurement Expert": "Negotiate vendor contracts. Focus on leverage and concessions.",
    "🏢 Startup Founder": "Investor negotiations. Focus on storytelling and strategic framing."
}

# --- SIDEBAR ---
st.sidebar.title("⚖️ Negotiation Suite")
selected_strategy = st.sidebar.selectbox("Select Expert Persona:", list(STRATEGIES.keys()))

# --- STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI ---
st.title(f"Sovereign Negotiator: {selected_strategy}")

# 1. STRATEGY BLUEPRINT
with st.expander("🚀 Build your Strategy Plan"):
    scenario = st.text_area("Describe your situation:")
    if st.button("Generate Plan"):
        with st.spinner("Generating..."):
            prompt = f"Act as {selected_strategy}. Instructions: {STRATEGIES[selected_strategy]}. Create a 3-step action plan for: {scenario}"
            try:
                # Use generate_content directly for one-off plans
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"API Error: {str(e)}")

# 2. CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask a follow-up question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        try:
            # Simple chat generation
            chat_prompt = f"Persona: {selected_strategy}. Context: {user_input}"
            response = model.generate_content(chat_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Rate limit reached. Please wait a moment and try again.")

# --- EXPORT ---
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("📥 Download Report", transcript, file_name="report.txt")