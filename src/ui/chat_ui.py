import streamlit as st

def render_chat_header():
    """
    Renders a sleek header for the chatbot app.
    """
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; background-color: #E3F2FD; border-radius: 12px; color: #0D47A1;">
            <h1>AI Virtual Assistant</h1>
            <p style="font-size: 14px;">Empowering your conversations with cutting-edge AI technology.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_chat_ui(chat_memory):
    """
    Renders the chat interface with a light and elegant design.
    Args:
        chat_memory: Instance of ChatMemory containing the chat history.
    """
    st.markdown("<h3 style='color: #0D47A1;'>Chat Log</h3>", unsafe_allow_html=True)

    history = chat_memory.get_history()

    if history:
        for entry in history:
            st.markdown(
                f"""
                <div style="padding: 15px; margin-bottom: 10px; background-color: #F1F8E9; border-left: 5px solid #76FF03; border-radius: 5px; color: #1B5E20;">
                    <p><strong>You:</strong> {entry['user']}</p>
                    <p><strong>Bot:</strong> {entry['bot']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<p style='color: #616161;'>No chat history yet. Start a conversation!</p>",
            unsafe_allow_html=True,
        )

    # Clear chat history button
    clear_button_style = """
        <style>
            div.stButton > button:first-child {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                cursor: pointer;
            }
            div.stButton > button:first-child:hover {
                background-color: #388E3C;
            }
        </style>
    """

    st.markdown(clear_button_style, unsafe_allow_html=True)

    if st.button("Clear History"):
        chat_memory.clear_history()
        st.session_state["chat_memory"] = chat_memory  # Reset session state
        st.success("Chat history has been cleared!")
