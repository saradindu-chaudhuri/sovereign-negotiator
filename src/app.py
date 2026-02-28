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

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ---------------------------------------------------------
# PERSONAS (Expanded for traction)
# ---------------------------------------------------------
STRATEGIES = {
    "💼 Corporate Attorney": "You are a top-tier corporate negotiator. Your tone is formal, precise, and authoritative. You focus on risk mitigation, contractual leverage, and maximizing ROI.",
    "🤝 Diplomatic Mediator": "You are a master mediator. You specialize in conflict de-escalation and finding the Zone of Possible Agreement (ZOPA).",
    "💰 Salary Maximizer": "You are a compensation strategist. You help users negotiate salary, equity, and bonuses using market data.",
    "🏗️ Procurement Expert": "You negotiate vendor contracts, pricing, SLAs, and long-term supply agreements. You focus on leverage, concessions, and value extraction.",
    "🏢 Startup Founder": "You negotiate with investors, partners, and early customers. You focus on storytelling, leverage, and strategic framing."
}

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("⚖️ Negotiation Suite")
selected_strategy = st.sidebar.selectbox("Select Expert Persona:", list(STRATEGIES.keys()))
st.sidebar.markdown("---")
st.sidebar.info("This tool generates high‑leverage negotiation strategies based on your unique scenario.")

# Coming Soon box (prepares users for monetization later)
st.sidebar.markdown("### 🔒 Coming Soon")
st.sidebar.markdown("""
- Unlimited chat  
- Advanced personas  
- Deep memory  
- PDF export  
- Strategy Packs  
""")

# ---------------------------------------------------------
# MODEL INIT
# ---------------------------------------------------------
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=STRATEGIES[selected_strategy]
)

# ---------------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------------
st.title(f"Sovereign Negotiator: {selected_strategy}")
st.subheader("Your AI‑Powered Strategic Edge")

# ---------------------------------------------------------
# SESSION STATE (Chat History)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# STRATEGY PLAN GENERATOR
# ---------------------------------------------------------
with st.expander("🚀 Build your Strategy Plan (Recommended first step)"):
    scenario = st.text_area("Describe your situation (goal, opponent, leverage):")

    if st.button("Generate Strategic Blueprint"):
        if scenario.strip():
            with st.spinner("Analyzing leverage and generating plan..."):
                prompt = (
                    f"As {selected_strategy}, create a structured negotiation plan.\n"
                    f"Include:\n"
                    f"- Leverage points\n"
                    f"- Risks\n"
                    f"- Counter‑moves\n"
                    f"- A 3‑step action plan\n\n"
                    f"Scenario: {scenario}"
                )
                response = model.generate_content(prompt)
                plan = response.text

                st.markdown(plan)
                st.session_state.messages.append({"role": "assistant", "content": plan})
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
if user_input := st.chat_input("Ask for a counter‑argument or negotiation tactic..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = model.generate_content(user_input)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# ---------------------------------------------------------
# FEEDBACK BOX (for traction + future monetization)
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 💬 Feedback")
feedback = st.text_input("What negotiation challenge are you facing? (Optional)")

if st.button("Submit Feedback"):
    if feedback.strip():
        st.success("Thank you — your feedback helps improve the tool!")
    else:
        st.warning("Please enter something before submitting.")

# ---------------------------------------------------------
# EXPORT (Free for now)
# ---------------------------------------------------------
if st.session_state.messages:
    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        label="📥 Download Negotiation Report",
        data=transcript,
        file_name=f"negotiation_report_{datetime.date.today()}.txt",
        mime="text/plain"
    )
