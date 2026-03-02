import streamlit as st
import google.generativeai as genai
import datetime

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sovereign Negotiator",
    layout="wide",
    page_icon="⚖️"
)

# ---------------------------------------------------------
# MODEL INITIALIZATION (CACHED)
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_model()

# ---------------------------------------------------------
# PERSONAS
# ---------------------------------------------------------
STRATEGIES = {
    "💼 Corporate Attorney": "You are a top-tier corporate negotiator. Formal, precise, authoritative. Focus on risk mitigation and ROI.",
    "🤝 Diplomatic Mediator": "You are a master mediator. Focus on de-escalation and finding the Zone of Possible Agreement (ZOPA).",
    "💰 Salary Maximizer": "You are a compensation strategist. Data-driven, assertive, focused on value proposition.",
    "🏗️ Procurement Expert": "You negotiate vendor contracts. Focus on leverage, concessions, and long-term value.",
    "🏢 Startup Founder": "You negotiate with investors. Focus on storytelling, leverage, and strategic framing."
}

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("⚖️ Negotiation Suite")
selected_strategy = st.sidebar.selectbox("Select Expert Persona:", list(STRATEGIES.keys()))
st.sidebar.markdown("---")
st.sidebar.info("This tool generates high-leverage negotiation strategies based on your unique scenario.")

# ---------------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------------
st.title(f"Sovereign Negotiator: {selected_strategy}")
st.subheader("Your AI-Powered Strategic Edge")

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ---------------------------------------------------------
# STRATEGY BUILDER
# ---------------------------------------------------------
with st.expander("🚀 Build your Strategy Plan (Recommended first step)"):
    scenario = st.text_area("Describe your situation (goal, opponent, leverage):")

    if st.button("Generate Strategic Blueprint"):
        if scenario.strip():
            with st.spinner("Analyzing leverage..."):
                prompt = (
                    f"Act as {selected_strategy}. "
                    f"Instructions: {STRATEGIES[selected_strategy]}. "
                    f"Create a structured 3-step negotiation plan for: {scenario}"
                )
                try:
                    response = st.session_state.chat.send_message(prompt)
                    plan = response.text
                    st.markdown(plan)
                    st.session_state.messages.append({"role": "assistant", "content": plan})
                except Exception:
                    st.error("The Negotiator is temporarily throttled. Please wait 30 seconds and try again.")
        else:
            st.warning("Please describe your scenario first.")

# ---------------------------------------------------------
# CHAT HISTORY DISPLAY
# ---------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------
if user_input := st.chat_input("Ask for a counter-argument or negotiation tactic..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(
                f"Persona: {STRATEGIES[selected_strategy]}. User input: {user_input}"
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.error("The Negotiator is temporarily throttled. Please wait 30 seconds and try again.")

# ---------------------------------------------------------
# EXPORT BUTTON
# ---------------------------------------------------------
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        "📥 Download Negotiation Report",
        transcript,
        file_name=f"report_{datetime.date.today()}.txt"
    )
