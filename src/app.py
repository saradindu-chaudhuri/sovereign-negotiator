import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Sovereign Negotiator Pro", layout="wide", page_icon="⚖️")
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- PROFESSIONAL PERSONAS ---
STRATEGIES = {
    "💼 Corporate Attorney": "You are a top-tier corporate negotiator. Your tone is formal, precise, and authoritative. You focus on risk mitigation, contractual leverage, and maximizing ROI. You do not offer fluff; you offer strategy.",
    "🤝 Diplomatic Mediator": "You are a master mediator. You specialize in conflict de-escalation and finding the 'Zone of Possible Agreement' (ZOPA). Your tone is empathetic, calm, and highly persuasive.",
    "💰 Salary Maximizer": "You are a career consultant and HR expert. You help users negotiate offers, equity, and bonuses by citing market data and emphasizing value proposition. You are assertive and data-driven."
}

# --- SIDEBAR UI ---
st.sidebar.title("⚖️ Negotiation Suite")
selected_strategy = st.sidebar.selectbox("Select Expert Persona:", list(STRATEGIES.keys()))
st.sidebar.markdown("---")
st.sidebar.info("This tool generates high-leverage negotiation strategies based on your unique scenario.")

# Initialize Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=STRATEGIES[selected_strategy]
)

# --- MAIN UI ---
st.title(f"Sovereign Negotiator: {selected_strategy}")
st.subheader("Your AI-Powered Strategic Edge")

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- THE "PRODUCT" HOOK: STRATEGY BUILDER ---
with st.expander("🚀 Build your Strategy Plan (Recommended first step)"):
    context = st.text_area("What is the scenario? (Goal, Opponent, Your Leverage):")
    if st.button("Generate Strategic Blueprint"):
        if context:
            with st.spinner("Analyzing leverage..."):
                prompt = f"Act as a {selected_strategy}. Create a 3-step strategy plan for this situation: {context}"
                response = model.generate_content(prompt)
                plan = response.text
                st.markdown(plan)
                st.session_state.messages.append({"role": "assistant", "content": plan})
        else:
            st.warning("Please enter your situation above.")

# --- CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask for a counter-argument or negotiation tactic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- EXPORT FEATURE (For Professional Deliverables) ---
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        label="📥 Download Negotiation Report",
        data=transcript,
        file_name=f"negotiation_report_{datetime.date.today()}.txt",
        mime="text/plain"
    )