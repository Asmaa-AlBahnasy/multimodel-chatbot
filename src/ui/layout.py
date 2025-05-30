import streamlit as st

def initialize_ui():
    """
    Initializes the Streamlit app UI with a clean and minimalist layout.
    """
    st.set_page_config(
        page_title="Smart AI Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar Header
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 20px; background-color: #F8F9FA; border-radius: 10px; color: #343A40;">
            <h2 style="color: #0D6EFD;">Smart AI Assistant</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Info Section
    st.sidebar.markdown(
        """
        <div style="padding: 15px; margin-bottom: 15px; background-color: #E9ECEF; border-radius: 10px; color: #495057;">
            <p style="font-size: 16px;">Enhance your productivity with state-of-the-art AI features.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Logo
    st.sidebar.image(
        "static/Logo.png", use_column_width=True, caption="Powered by Innovation"
    )

