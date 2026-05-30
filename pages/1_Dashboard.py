import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dashboard RCV",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* ==========================
   CONTENIDO PRINCIPAL
========================== */

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

/* ==========================
   SIDEBAR
========================== */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1D3557 0%, #457B9D 100%);
}

/* Texto blanco */
[data-testid="stSidebar"],
[data-testid="stSidebar"] * {
    color: white !important;
}

/* ==========================
   BOTONES APP / DASHBOARD
========================== */

[data-testid="stSidebarNav"] a {
    background-color: #DE7A24 !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: #F28E2B !important;
}

[data-testid="stSidebarNav"] span {
    color: white !important;
    font-weight: 600 !important;
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