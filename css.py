css_code="""
    <style>
        /* Styling for all containers inside the main section */
        div.stMainBlockContainer div[data-testid="stVerticalBlock"] {
            background: rgb(38, 39, 48);
            padding: 2rem !important;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* Header styling */
        header.stAppHeader {
            background: transparent !important;
        }

        /* Target all element containers */
        div[data-testid="stElementContainer"][width] {
            width: auto !important;
            max-width: 100% !important;
        }

        /* Optional: make tables and charts inside behave responsively too */
        div[data-testid="stElementContainer"] > div {
            max-width: 100% !important;
        }
        
        /* Heading (h3) styling */
        div[data-testid="stHeadingWithActionElements"] h3 {
            color: rgb(197, 44, 95) !important;
        }
    </style>
    """