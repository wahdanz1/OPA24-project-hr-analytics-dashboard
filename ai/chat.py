import streamlit as st
from gemini import GeminiHandler  # adjust import path if needed
from pathlib import Path
import sys
import pandas as pd # Make sure pandas is imported

sys.path.append(str(Path(__file__).resolve().parent.parent))
from dashboard.utils import fetch_data_from_db

# Initialize the gemini handler
gemini_handler = GeminiHandler()

# Set the layout of the Streamlit app to wide
st.set_page_config(layout="wide")

# Initialize the session state for messages, df, and graph
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am a statistical consultant. How can I help you today?"}
    ]
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()  # Initialize with an empty DataFrame
if "graph" not in st.session_state:
    st.session_state.graph = None # Initialize graph to None or False

col1, col2 = st.columns([1, 1])

with col1:
    # Use a container for the chat history to enable scrolling
    with st.container(height=540, border=False): # You can adjust the height as needed
        # Display the chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

with col2:
    # Only display Data Preview if the DataFrame is not empty
    if not st.session_state.df.empty: # FIX: Check if DataFrame is actually not empty
        with st.container(height=540, border=True): # You can adjust the height as needed
            st.write("### Data Preview")
            # st.session_state.get("df") is redundant here, st.session_state.df is fine
            st.dataframe(st.session_state.df) # Streamlit's default dataframe will handle its own scrolling if it's too big
    
    # Only display Graph Preview if a graph has been set
    if st.session_state.graph: # This condition will now work if graph is set to a truthy value
        st.write("### Graph Preview")
        with st.container(height=540, border=True):
            # You would display your graph here, e.g., st.pyplot(st.session_state.graph)
            # For now, it's just 'pass' as the graph generation logic isn't provided.
            pass

# Chat input

prompt = st.chat_input("Ask a question about the data", key="chat_input")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})



    df = st.session_state.df  # Get the current DataFrame from session state
    response = gemini_handler.get_response(prompt, st.session_state.messages,csv_string=df.to_csv(index=False) if not df.empty else None)
    
    if response and response.get("query"): # Ensure response is not None and has 'query' key
        try:
            # Attempt to fetch data from DB
            df = fetch_data_from_db(response["query"])
            st.session_state.df = df # Store the DataFrame in session state (overwrites previous)
            st.session_state.messages.append({"role": "assistant", "content": response.get("response", "Query executed successfully.")})
            


        except Exception as db_error: # <--- THIS IS WHERE THE DATABASE ERROR IS CAUGHT
            # Convert the exception object to a string to inspect its content
            error_string = str(db_error)
            
            # Now you can check for specific substrings within the error_string
            if "Binder Error: No function matches the given name and argument types 'lower(BOOLEAN)'" in error_string:
                # This is the specific error you're looking for
                specific_db_error_message = "The query tried to use 'lower()' on a non-string column (likely boolean). Gemini needs to adjust the query."
                st.session_state.messages.append({"role": "assistant", "content": f"Database query failed: {specific_db_error_message}"})
                # You could then potentially trigger a specific re-prompt for Gemini here
                # (This is where the retry loop logic from our previous discussion would come in)
            elif "syntax error" in error_string.lower():
                # Generic SQL syntax error
                st.session_state.messages.append({"role": "assistant", "content": f"Database query failed due to a SQL syntax error."})
            else:
                # Catch-all for other database errors
                st.session_state.messages.append({"role": "assistant", "content": f"Database query failed with an unexpected error: {error_string}"})


    else: # Gemini did not provide a query or gave an irrelevant response
        # Add assistant message (if no query was generated)
        st.session_state.messages.append({"role": "assistant", "content": response.get("response", "I didn't generate a query or encountered an internal error.")})
        with st.chat_message("assistant"):
            st.markdown(response.get("response", "I didn't generate a query or encountered an internal error."))
    
    # TODO: Add logic here to set st.session_state.graph if a graph is generated by gemini_handler
    # For example:
    # if response["graph_data"]:
    #     fig = create_plot_from_data(response["graph_data"]) # You'd need a function for this
    #     st.session_state.graph = fig

    
    st.rerun() # Rerun to update the UI with new messages, df, or graph