import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Dashboard RCV · Power BI", layout="wide")

components.iframe(
    src="https://app.powerbi.com/view?r=eyJrIjoiMWM3ZTk4ZTYtYzY4ZC00MDYxLWI2NjYtNGE4NjhjZTViZjAzIiwidCI6ImUzOGI2YjNiLWRkMTQtNDVhZi1hZjBhLWU2N2QxYjk2ODQyYSIsImMiOjR9&navContentPaneEnabled=false",
    height=800,
    scrolling=False
)