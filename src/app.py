import streamlit as st
import google.generativeai as genai
import datetime
import time

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Sovereign Negotiator", layout="wide", page_icon="⚖️")

MODEL_NAME = "gemini-1.5-flash"

@st.cache_resource
def get_model():
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    return genai.GenerativeModel(MODEL_NAME)

model = get_model()

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

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "cooldown" not in st.session_state:
    st.session_state.cooldown = 0

def safe_send(prompt):
    now = time.time()
    if now < st.session_state.cooldown:
        raise Exception("cooldown")

    try:
        response = st.session_state.chat.send_message(prompt)
        st.session_state.cooldown = time.time() + 2
        return response.text
    except:
        st.session_state.cooldown = time.time() + 5
        raise

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
                    f"Create a 3-step action plan for: {scenario}"
                )
                try:
                    plan = safe_send(prompt)
                    st.markdown(plan)
                    st.session_state.messages.append({"role": "assistant", "content": plan})
                except:
                    st.error("Negotiator is busy. Please wait 5 seconds and try again.")
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

    with st.chat_message("assistant"):
        try:
            reply = safe_send(
                f"Persona: {selected_strategy}. User: {user_input}"
            )
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except:
            st.error("Negotiator is busy. Please wait 5 seconds and try again.")

# ---------------------------------------------------------
# EXPORT
# ---------------------------------------------------------
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("📥 Download Report", transcript, file_name="negotiation_report.txt")
