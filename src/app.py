import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Sovereign Negotiator", layout="wide", page_icon="⚖️")

# --- MODEL INITIALIZATION (Cached for Stability) ---
@st.cache_resource
def get_model():
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

# --- PERSONAS ---
STRATEGIES = {
    "💼 Corporate Attorney": "You are a top-tier corporate negotiator. Formal, precise, authoritative. Focus on risk mitigation and ROI.",
    "🤝 Diplomatic Mediator": "You are a master mediator. Focus on de-escalation and finding the Zone of Possible Agreement (ZOPA).",
    "💰 Salary Maximizer": "You are a compensation strategist. Data-driven, assertive, focused on value proposition.",
    "🏗️ Procurement Expert": "You negotiate vendor contracts. Focus on leverage, concessions, and long-term value.",
    "🏢 Startup Founder": "You negotiate with investors. Focus on storytelling, leverage, and strategic framing."
}

# --- SIDEBAR UI ---
st.sidebar.title("⚖️ Negotiation Suite")
selected_strategy = st.sidebar.selectbox("Select Expert Persona:", list(STRATEGIES.keys()))
st.sidebar.markdown("---")
st.sidebar.info("This tool generates high-leverage negotiation strategies based on your unique scenario.")

# --- MAIN UI ---
st.title(f"Sovereign Negotiator: {selected_strategy}")
st.subheader("Your AI-Powered Strategic Edge")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STRATEGY BUILDER ---
with st.expander("🚀 Build your Strategy Plan (Recommended first step)"):
    scenario = st.text_area("Describe your situation (goal, opponent, leverage):")
    if st.button("Generate Strategic Blueprint"):
        if scenario.strip():
            with st.spinner("Analyzing leverage..."):
                prompt = f"Act as {selected_strategy}. Instructions: {STRATEGIES[selected_strategy]}. Create a 3-step action plan for: {scenario}"
                try:
                    response = model.generate_content(prompt)
                    plan = response.text
                    st.markdown(plan)
                    st.session_state.messages.append({"role": "assistant", "content": plan})
                except Exception as e:
                    st.error("The Negotiator is temporarily throttled. Please wait 30 seconds and try again.")
        else:
            st.warning("Please describe your scenario first.")

# --- CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask for a counter-argument or negotiation tactic..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # We must pass the system instruction as a configuration for the prompt
            chat = model.start_chat(history=[])
            response = chat.send_message(f"Persona: {STRATEGIES[selected_strategy]}. User input: {user_input}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("The Negotiator is temporarily throttled. Please wait 30 seconds and try again.")

# --- EXPORT ---
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("📥 Download Negotiation Report", transcript, file_name=f"report_{datetime.date.today()}.txt")