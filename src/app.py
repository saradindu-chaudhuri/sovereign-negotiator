import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize the model with a clear persona
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=(
        "You are a brilliant, calm, and strategic sovereign negotiator. "
        "Your goal is to find win-win solutions while maintaining high ethical standards. "
        "Keep responses concise, professional, and firm."
    )
)
# 3. Your function to get a response
def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# 4. Streamlit UI
st.title("Sovereign Negotiator")
user_input = st.text_input("Enter your negotiation prompt:")

if st.button("Negotiate"):
    if user_input:
        answer = get_ai_response(user_input)
        st.write(answer)
    else:
        st.warning("Please enter a prompt first.")