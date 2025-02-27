import google.generativeai as genai
import streamlit as st
from streamlit_chat import message

# Configure API (Replace with a secured method)
api_key = 'AIzaSyDuPBbp8To3hJRVp4IXIZheAxLe4i4GcKo'  # Use a secure method to store API keys
genai.configure(api_key=api_key)

# Define safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# Initialize the generative model with safety settings
model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)

# Streamlit UI Configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

# Title
st.title("🤖 Gemini AI Chatbot")
st.markdown("Engage with an AI-powered chatbot using Google's Gemini-1.5 Flash!")

# Initialize chat history session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history (messages at the top)
st.markdown("### Chat History")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        message(chat["content"], is_user=True)
    else:
        message(chat["content"], is_user=False)

# User input at the bottom
user_input = st.text_input("Type your message and press Enter:")

if user_input:
    # Avoid duplicate input processing
    if "last_input" in st.session_state and st.session_state.last_input == user_input:
        # st.warning("Same input detected, preventing duplicate processing.")
        pass
    else:
        st.session_state.last_input = user_input  # Store last input

        with st.spinner("Thinking..."):
            # Correct chat history format
            formatted_history = [
                {"role": msg["role"], "parts": [{"text": msg["content"]}]} 
                for msg in st.session_state.chat_history
            ]

            chat = model.start_chat(history=formatted_history)
            response = chat.send_message(user_input, stream=True)
            
            answer = ""
            for chunk in response:
                answer += chunk.text
            
            # Append messages to session state
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "model", "content": answer})

        st.rerun()

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.last_input = None  # Reset last input
    st.rerun()

# Footer
st.markdown("---")
