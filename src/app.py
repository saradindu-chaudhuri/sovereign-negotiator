import streamlit as st
import google.generativeai as genai
import datetime

# 1. Config and Setup
st.set_page_config(page_title="Sovereign Negotiator Pro", layout="wide")
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Define Personas
MODES = {
    "Salary Negotiation": "You are a world-class HR and Career Consultant. You help users maximize their compensation packages, including equity, bonuses, and benefits. You are data-driven, firm, and value-focused.",
    "Business/Contract": "You are a sharp corporate attorney and strategist. You identify leverage, mitigate risk, and structure deals for maximum ROI. You speak in legal/business terminology.",
    "Rental/Lease": "You are a real estate expert. You identify red flags in leases and help tenants negotiate lower rent or better terms by citing market trends and local laws."
}

# 3. Sidebar Setup
st.sidebar.title("🛠️ Negotiation Suite")
selected_mode = st.sidebar.selectbox("Select Strategy Mode:", list(MODES.keys()))
st.sidebar.info("Select a mode to initialize the expert persona.")

# 4. Initialize Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=MODES[selected_mode]
)

# 5. App UI
st.title(f"⚖️ Sovereign Negotiator: {selected_mode}")
st.markdown("---")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Strategic Planner (The "Revenue" Feature)
with st.expander("🚀 Generate Strategy Plan (Before you start)"):
    context = st.text_area("Tell me your situation (Opponent, Goal, Your Leverage):")
    if st.button("Create Strategy Plan"):
        with st.spinner("Analyzing leverage..."):
            strategy_prompt = f"Analyze this situation and create a 3-step negotiation strategy plan for a {selected_mode}. Situation: {context}"
            plan = model.generate_content(strategy_prompt)
            st.write(plan.text)
            st.session_state.messages.append({"role": "assistant", "content": plan.text})

# 7. Chat Interface
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

# 8. Pro Export Feature
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        label="📥 Download Negotiation Report",
        data=transcript,
        file_name=f"negotiation_{datetime.date.today()}.txt",
        mime="text/plain"
    )