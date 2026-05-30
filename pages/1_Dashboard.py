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

/* Permitir ver el header para que no se destruya el botón, pero ocultamos su fondo decorativo nativo */
header {
    visibility: visible !important;
    background: transparent !important;
}

footer, #MainMenu {
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

/* ==========================================
   AGREGADO: CONTROL EXCLUSIVO DEL BOTÓN ILUMINADO
========================================== */

button[kind="header"],
[data-testid="collapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {
    opacity: 1 !important;
    visibility: visible !important;
    display: flex !important;
    z-index: 99999 !important;
    background-color: rgba(255, 255, 255, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="collapsedControl"] button svg,
button[kind="header"] svg {
    fill: #ffffff !important;
    stroke: #ffffff !important;
    color: #ffffff !important;
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