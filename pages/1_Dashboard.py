import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dashboard RCV",
    layout="wide"
)

# Ocultar márgenes y menú de Streamlit
st.markdown("""
<style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }

    header, footer, #MainMenu {
        visibility: hidden;
    }

    iframe {
        border: none;
    }
</style>
""", unsafe_allow_html=True)

components.html(
    """
    <iframe
        title="Dashboard RCV"
        width="100%"
        height="950"
        src="https://app.powerbi.com/view?r=eyJrIjoiMWM3ZTk4ZTYtYzY4ZC00MDYxLWI2NjYtNGE4NjhjZTViZjAzIiwidCI6ImUzOGI2YjNiLWRkMTQtNDVhZi1hZjBhLWU2N2QxYjk2ODQyYSIsImMiOjR9"
        frameborder="0"
        allowfullscreen="true">
    </iframe>
    """,
    height=950
)