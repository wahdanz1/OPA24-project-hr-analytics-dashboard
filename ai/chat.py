import streamlit as st
from .gemini import GeminiHandler  # adjust import path if needed
from pathlib import Path
import sys
import pandas as pd # Make sure pandas is imported

sys.path.append(str(Path(__file__).resolve().parent.parent))
from dashboard.utils import fetch_data_from_db
from dashboard.plots import create_horizontal_bar_chart, create_vertical_bar_chart, create_line_chart

def open_chat():

    # Initialize the gemini handler
    gemini_handler = GeminiHandler()

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
        if not st.session_state.df.empty: # Check if DataFrame is actually not empty
            graph_tab, data_tab = st.tabs(["Graph Preview", "Data Preview"])
            with graph_tab:
                # Display the graph if it exists
                if st.session_state.graph: # This condition will now work if graph is set to a truthy value
                    st.plotly_chart(st.session_state.graph, use_container_width=True)
            with data_tab:
                # Display the DataFrame preview
                st.write("### Data Preview")
                st.dataframe(st.session_state.df) # Streamlit's default dataframe will handle its own scrolling if it's too big

        

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
                # Debug prnt the query to see what Gemini generated
                st.session_state.messages.append({"role": "assistant", "content": f"Executing query: {response['query']}"})
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
        
        if response and response.get("methods"): # Ensure response is not None and has 'methods' key
            # Process the methods to generate a graph
            for method in response["methods"]:
                if method["name"] == "create_horizontal_bar_chart":
                    st.session_state.graph = create_horizontal_bar_chart(
                        data=df,
                        x_value=method["args"]["x_value"],
                        y_value=method["args"]["y_value"],
                        title="Requested Chart",
                        #color_column=method["args"].get("color_column", None),  # Optional color column
                        x_label=method["args"].get("x_label", "X-axis"),
                        y_label=method["args"].get("y_label", "Y-axis"),
                    )
                elif method["name"] == "create_vertical_bar_chart":
                    st.session_state.graph = create_vertical_bar_chart(
                        data=df,
                        x_value=method["args"]["x_value"],
                        y_value=method["args"]["y_value"],
                        title="Requested Chart",
                        #color_column=method["args"].get("color_column", None),  # Optional color column
                        x_label=method["args"].get("x_label", "X-axis"),
                        y_label=method["args"].get("y_label", "Y-axis"),
                    )
                elif method["name"] == "create_line_chart":
                    st.session_state.graph = create_line_chart(
                        data=df,
                        x_value=method["args"]["x_value"],
                        y_value=method["args"]["y_value"],
                        title="Requested Chart",
                        #color_column=method["args"].get("color_column", None),  # Optional color column
                        x_label=method["args"].get("x_label", "X-axis"),
                        y_label=method["args"].get("y_label", "Y-axis"),
                    )

        
        st.rerun() # Rerun to update the UI with new messages, df, or graph
        