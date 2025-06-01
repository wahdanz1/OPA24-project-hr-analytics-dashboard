# CSS code file
# all_css_code="""
#     <style>
#         /* Styling for all containers inside the main section */
#         div.stMainBlockContainer div[data-testid="stVerticalBlock"] {
#             background: rgb(38, 39, 48);
#             padding: 2rem !important;
#             border-radius: 10px;
#             border: 1px solid rgba(255,255,255,0.1);
#         }

#         /* Header styling */
#         header.stAppHeader {
#             background: transparent !important;
#         }

#         /* Target all element containers */
#         div[data-testid="stElementContainer"][width] {
#             width: auto !important;
#             max-width: 100% !important;
#         }

#         /* Optional: make tables and charts inside behave responsively too */
#         div[data-testid="stElementContainer"] > div {
#             max-width: 100% !important;
#         }
        
#         /* Heading (h3) styling */
#         div[data-testid="stHeadingWithActionElements"] h3 {
#             color: rgb(197, 44, 95) !important;
#         }

#         /* Button styling (custom buttons) */
#         .dbt-button {
#             font-size: 16px;
#             padding: 10px;
#             background-color: rgb(60, 62, 76);
#             color: white;
#             border-radius: 8px;
#             border-style: solid;
#             border-width: 1px;
#             border-color: rgba(255, 255, 255, 0.2);
#             cursor: pointer;
#             transition: border-color 0.2s ease;
#         }

#         .dbt-button:hover {
#             border-color: rgb(197, 44, 95);
#         }

#         .dbt-button:active {
#             border-color: rgb(197, 44, 95);
#         }
#     </style>
#     """

prefix="""
    <style>
    """

suffix="""
    </style>
    """

container_styling="""
        /* Styling for all containers inside the main section */
        div.stMainBlockContainer div[data-testid="stVerticalBlock"] {
            background: rgb(38, 39, 48);
            padding: 0.5rem 2rem 2rem !important;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
        }
    """

header_styling="""
        /* Header styling */
        header.stAppHeader {
            background: transparent !important;
        }
        
        /* Heading (h3) styling */
        div[data-testid="stHeadingWithActionElements"] h3 {
            color: rgb(197, 44, 95) !important;
        }
    """

element_container_styling="""
        /* Set element containers' width */
        div[data-testid="stElementContainer"][width] {
            width: auto !important;
            max-width: 100% !important;
        }

        /* Optional: make tables and charts inside behave responsively too */
        div[data-testid="stElementContainer"] > div {
            max-width: 100% !important;
        }
    """

button_styling="""
        /* Button styling (custom buttons) */
        .dbt-button {
            font-size: 16px;
            padding: 10px;
            background-color: rgb(60, 62, 76);
            color: white;
            border-radius: 8px;
            border-style: solid;
            border-width: 1px;
            border-color: rgba(255, 255, 255, 0.2);
            cursor: pointer;
            transition: border-color 0.2s ease;
        }

        .dbt-button:hover {
            border-color: rgb(197, 44, 95);
        }

        .dbt-button:active {
            border-color: rgb(197, 44, 95);
        }
    """
