import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Initialize the model (using Flash for speed)
model = genai.GenerativeModel('gemini-1.5-flash')

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