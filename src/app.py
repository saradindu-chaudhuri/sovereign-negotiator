import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize the model with a clear persona
# 1. THE DIPOMATIC MEDIATOR
persona = "You are a master mediator. Focus on de-escalation, active listening, and finding the 'zone of possible agreement' (ZOPA) where both sides benefit."
# Apply the instruction
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=persona
)
)
# 3. Your function to get a response
def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# 4. Streamlit UI
st.title("Sovereign Negotiator")
user_input = st.text_input("Enter your negotiation prompt:")

# 1. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle new input
if prompt := st.chat_input("Negotiate your terms..."):
    # Display user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    
    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": response.text})