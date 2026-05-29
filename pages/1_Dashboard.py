import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Dashboard RCV", layout="wide")

st.markdown("""
<style>
    .block-container { padding: 0 !important; margin: 0 !important; }
    iframe { border: none !important; display: block; }
</style>
""", unsafe_allow_html=True)

components.iframe(
    src="https://app.powerbi.com/view?r=eyJrIjoiMWM3ZTk4ZTYtYzY4ZC00MDYxLWI2NjYtNGE4NjhjZTViZjAzIiwidCI6ImUzOGI2YjNiLWRkMTQtNDVhZi1hZjBhLWU2N2QxYjk2ODQyYSIsImMiOjR9&navContentPaneEnabled=false",
    height=750,
    scrolling=False
)