import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Your function to get a response
def get_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# 4. Use it in your UI
st.title("Sovereign Negotiator")
user_input = st.text_input("Enter your negotiation prompt:")

if st.button("Negotiate"):
    answer = get_ai_response(user_input)
    st.write(answer)