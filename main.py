import streamlit as st

# Page Configuration
st.set_page_config(page_title="ANTNA Portal", page_icon="🐜", layout="centered")

# Title and Subheader
st.title("Welcome to ANTNA Portal 🐜")
st.subheader("Please select your role:")

# CSS for styling buttons (optional for better look)
st.markdown(
    """
    <style>
    .button {
        display: inline-block;
        padding: 15px 25px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: #fff;
        background-color: #4CAF50;
        border: none;
        border-radius: 15px;
        box-shadow: 0 9px #999;
        margin: 20px;
    }
    .button:hover {background-color: #45a049}
    .button:active {
        background-color: #45a049;
        box-shadow: 0 5px #666;
        transform: translateY(4px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display role selection buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("I am a Customer", use_container_width=True):
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=https://antnab.streamlit.app/">',
            unsafe_allow_html=True,
        )

with col2:
    if st.button("I am a First Responder", use_container_width=True):
        st.write("The First Responder portal is under construction!")  # Update with appropriate action
