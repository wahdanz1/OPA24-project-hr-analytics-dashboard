import streamlit as st
from gemini import GeminiHandler  # adjust import path if needed
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dashboard.utils import fetch_data_from_db
# Initialize the gemini handler
gemini_handler = GeminiHandler()

# Set the layout of the Streamlit app
st.set_page_config(layout="wide")

# Initialize the session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am a statistical consultant. How can I help you today?"}
    ]

# Display the chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask a question about the data", key="chat_input")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = gemini_handler.get_response(prompt, st.session_state.messages)

    if response["query"]:
        df = fetch_data_from_db(response["query"])
        csv_string = df.to_csv(index=False)
        st.write("### Query Result")
        st.dataframe(df)


    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response["response"]})
    with st.chat_message("assistant"):
        st.markdown(response["response"])
    

