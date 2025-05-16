import streamlit as st
st.set_page_config(layout="wide")
import plotly.express as px
import pandas as pd
from gemini import GeminiHandler
gemini = GeminiHandler()



if "messages" not in st.session_state:
    st.session_state.messages = []
st.header("Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Writes the users message 
        with st.chat_message("user"):
            st.markdown(prompt)
        # Writes the assistants response
        with st.chat_message("assistant"):
            response = gemini.get_response(prompt)
            st.markdown(response.text)
        # Adds last prompt + response to messages list
        st.session_state.messages.append({"role": "assistant", "content": response.text})

