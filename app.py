import streamlit as st
import google.generativeai as genai

# ---------------- CONFIGURATION ----------------
API_KEY = st.secrets["API_KEY"]

genai.configure(api_key=API_KEY)

business_info = """
You are the AI assistant for 'Ritul's Gym'. 
Here are the facts you MUST know:
- Timings: 6 AM to 10 PM, Monday to Saturday. Closed on Sunday.
- Fees: ₹1500/month, ₹4000/3 months.
- Trainers: Ravi (Cardio), Sunny (Weights).
- Rule: If asked anything outside of these facts, politely say 'Please call the gym for that info.'
"""

model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=business_info)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- UI ----------------
st.title("🤖 Ritul's AI Chatbot")
st.write("Built with Python, Streamlit & Gemini")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Type your message...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save for Streamlit
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Save for Gemini
    st.session_state.chat_history.append(
        {
            "role": "user",
            "parts": [prompt]
        }
    )

    # Generate response
    response = model.generate_content(st.session_state.chat_history)
    response_text = response.text

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Save for Streamlit
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )

    # Save for Gemini
    st.session_state.chat_history.append(
        {
            "role": "model",
            "parts": [response_text]
        }
    )
