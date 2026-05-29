"""
app.py — Aplicación Streamlit para predicción de Riesgo Cardiovascular
Uso: streamlit run app.py
"""

import json
import os

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Clasificador de Riesgo Cardiovascular",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Encuentra la sección después de st.set_page_config (alrededor de la línea 22)
# y AGREGA este código CSS:

st.set_page_config(
    page_title="Clasificador de Riesgo Cardiovascular",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS PARA SIDEBAR
# ──────────────────────────────────────────────

st.markdown("""
<style>
    /* Fondo del sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1D3557 0%, #457B9D 100%);
    }

    /* ── TODOS los textos del sidebar en blanco por defecto ── */
    [data-testid="stSidebar"] {
        color: white !important;
    }

    /* Labels (títulos de cada campo) siempre blancos */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] p {
        color: white !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        line-height: 1.1 !important;
        margin-bottom: 0px !important;
    }

    /* Subheaders blancos */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 700 !important;
        margin-top: 10px !important;
        margin-bottom: 2px !important;
        font-size: 0.82rem !important;
    }

    /* ── NUMBER INPUT ── */
    [data-testid="stSidebar"] input[type="number"] {
        background-color: rgba(255, 255, 255, 0.92) !important;
        color: #1D3557 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        height: 28px !important;
        padding: 2px 8px !important;
        font-size: 0.78rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] > div {
        height: 30px !important;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button {
        height: 28px !important;
        width: 24px !important;
        padding: 0 !important;
        background-color: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: none !important;
    }

    /* Contenedor del selectbox — permitir que el texto respire */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.92) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        min-height: 30px !important;
        height: 30px !important;
        display: flex !important;
        align-items: center !important;
        overflow: visible !important;
    }

    /* Texto seleccionado centrado verticalmente */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [class*="singleValue"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [class*="placeholder"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] input {
        color: #1D3557 !important;
        font-size: 0.75rem !important;
        line-height: 30px !important;
        overflow: visible !important;
    }

    /* Flecha del selectbox */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] svg {
        fill: #1D3557 !important;
    }

    /* Menú desplegable */
    [data-baseweb="popover"] ul li,
    [data-baseweb="menu"] ul li,
    [data-baseweb="popover"] li {
        color: #1D3557 !important;
        font-size: 0.75rem !important;
    }

    /* ── REDUCIR ESPACIADO ── */
    [data-testid="stSidebar"] .stElementContainer {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }

    [data-testid="stSidebar"] .stNumberInput,
    [data-testid="stSidebar"] .stSelectbox {
        margin-bottom: 3px !important;
        padding-bottom: 0px !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0px !important;
    }

    [data-testid="stSidebar"] .element-container {
        margin-bottom: 2px !important;
    }

    /* ── BOTÓN PREDECIR ── */
    [data-testid="stSidebar"] button[kind="primary"] {
        background-color: #DE7A24 !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
    }

    /* ── PADDING GENERAL ── */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.8rem !important;
        padding-bottom: 1rem !important;
    }
            
    /* Botones app y Dashboard del sidebar */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
    [data-testid="stSidebar"] nav a,
    [data-testid="stSidebar"] nav span {
        color: white !important;
        background-color: #DE7A24 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────
# CARGA DE ARTEFACTOS
# ──────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

@st.cache_resource
def cargar_modelo():
    modelo  = joblib.load(os.path.join(MODELS_DIR, "modelo_rf.joblib"))
    scaler  = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
    le      = joblib.load(os.path.join(MODELS_DIR, "label_encoder.joblib"))
    with open(os.path.join(MODELS_DIR, "feature_names.json")) as f:
        feature_names = json.load(f)
    return modelo, scaler, le, feature_names


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
COLORES_RIESGO = {
    "ALTO":  ("#FF4B4B", "🔴"),
    "MEDIO": ("#FFA500", "🟠"),
    "BAJO":  ("#00C853", "🟢"),
}

def color_riesgo(clase: str):
    return COLORES_RIESGO.get(clase.upper(), ("#888888", "⚪"))


def preparar_fila(datos_usuario: dict, feature_names: list) -> pd.DataFrame:
    """
    Convierte el dict con los valores del usuario en un DataFrame
    con exactamente las columnas que espera el modelo
    (one-hot encoding + orden correcto).
    """
    fila = pd.DataFrame([datos_usuario])

    # One-hot encoding solo de categóricas (CATEGORIA_IMC)
    categoricas = fila.select_dtypes(include=["object"]).columns.tolist()
    fila = pd.get_dummies(fila, columns=categoricas, drop_first=True)

    # Alinear con las columnas del entrenamiento
    fila = fila.reindex(columns=feature_names, fill_value=0)
    return fila


# ──────────────────────────────────────────────
# INTERFAZ
# ──────────────────────────────────────────────
def main():
    # ── Cabecera ──────────────────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1D3557 0%, #0088AD 100%);
        border-radius: 14px;
        padding: 28px 36px;
        margin-bottom: 24px;
        color: white;
    ">
        <div style="display:flex; align-items:center; gap:16px;">
            <span style="font-size:3rem;">🫀</span>
            <div>
                <h1 style="margin:0; font-size:1.9rem; font-weight:800;">
                    Clasificador de Riesgo Cardiovascular
                </h1>
                <p style="margin:6px 0 0 0; font-size:1rem; opacity:0.88;">
                    Ingresa los datos del paciente en el panel lateral y presiona 
                    <b>Predecir</b> para obtener la clasificación de riesgo cardiovascular.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Carga del modelo ──────────────────────
    try:
        modelo, scaler, le, feature_names = cargar_modelo()
    except FileNotFoundError:
        st.error(
            "⚠️ No se encontraron los artefactos del modelo. "
            "Ejecuta primero: `python src/train.py --data data/Clasificacion_RCV_Completo.xlsx`"
        )
        st.stop()

    # ── Sidebar — Datos del paciente ──────────
    st.sidebar.header("📋 Datos del paciente")

    with st.sidebar:

        st.subheader("Datos antropométricos")
        edad  = st.number_input("Edad (años)",  min_value=1,    max_value=120,   value=45,    step=1)
        peso  = st.number_input("Peso (kg)",    min_value=20.0, max_value=300.0, value=75.0,  step=0.1)
        talla = st.number_input("Talla (cm)",   min_value=50.0, max_value=250.0, value=170.0, step=0.1)
        imc   = st.number_input(
            "IMC (kg/m²)",
            min_value=10.0, max_value=80.0,
            value=round(peso / (talla / 100) ** 2, 1),
            step=0.1
        )
        cat_imc = st.selectbox(
            "Categoría IMC",
            # ⚠️ Verifica con: df["CATEGORIA_IMC"].unique()
            ["Normal", "Sobrepeso", "Obesidad", "Bajo peso"]
        )

        st.subheader("Perfil lipídico")
        col_hdl   = st.number_input("Colesterol HDL (mg/dL)",   min_value=20.0,  max_value=200.0,  value=50.0,  step=0.1)
        col_ldl   = st.number_input("Colesterol LDL (mg/dL)",   min_value=20.0,  max_value=400.0,  value=100.0, step=0.1)
        trigli    = st.number_input("Triglicéridos (mg/dL)",    min_value=20.0,  max_value=1000.0, value=150.0, step=0.1)
        col_total = st.number_input("Colesterol total (mg/dL)", min_value=50.0,  max_value=500.0,  value=180.0, step=0.1)

        st.subheader("Presión arterial")
        pas = st.number_input("Presión sistólica (mmHg)",  min_value=60.0,  max_value=250.0, value=120.0, step=0.1)
        pad = st.number_input("Presión diastólica (mmHg)", min_value=40.0,  max_value=150.0, value=80.0,  step=0.1)

        st.subheader("Función renal")
        creat = st.number_input("Creatinina sérica (mg/dL)", min_value=0.1, max_value=20.0, value=1.0, step=0.01)

        st.subheader("Antecedentes")
        sexo       = st.selectbox("Sexo",             [0, 1], format_func=lambda x: "Femenino" if x == 0 else "Masculino")
        tabaquismo = st.selectbox(
            "Hábito tabáquico",
            [0, 1, 2, 3],
            format_func=lambda x: {0: "No fumador", 1: "Ex fumador", 2: "Fumador ocasional", 3: "Fumador habitual"}.get(x, str(x))
        )
        diabetes   = st.selectbox("Diabetes",         [0, 1], format_func=lambda x: "No" if x == 0 else "Sí")

        predecir_btn = st.button("🔍 Predecir riesgo", use_container_width=True, type="primary")

    # ── Panel principal ───────────────────────
    col_resumen, col_detalle = st.columns([1, 2])

    with col_resumen:
        st.markdown("""
        <div style="background:#EEF6FA; border-left:5px solid #0088AD;
                    border-radius:6px; padding:14px 18px; margin-bottom:14px;">
            <p style="margin:0; color:#1D3557; font-size:0.9rem; font-weight:600;">
                📋 Resumen del paciente
            </p>
        </div>
        """, unsafe_allow_html=True)

        resumen = [
            ("Edad",          f"{edad} años"),
            ("Peso",          f"{peso} kg"),
            ("Talla",         f"{talla} cm"),
            ("IMC",           f"{imc:.1f} kg/m²"),
            ("Categoría IMC", cat_imc),
            ("Col. HDL",      f"{col_hdl:.1f} mg/dL"),
            ("Col. LDL",      f"{col_ldl:.1f} mg/dL"),
            ("Triglicéridos", f"{trigli:.1f} mg/dL"),
            ("Col. Total",    f"{col_total:.1f} mg/dL"),
            ("P. Sistólica",  f"{pas:.1f} mmHg"),
            ("P. Diastólica", f"{pad:.1f} mmHg"),
            ("Creatinina",    f"{creat:.2f} mg/dL"),
            ("Sexo",          "Masculino" if sexo == 1 else "Femenino"),
            ("Tabaquismo",    {0: "No fumador", 1: "Ex fumador",
                            2: "Fumador ocasional", 3: "Fumador habitual"}.get(tabaquismo, str(tabaquismo))),
            ("Diabetes",      "Sí" if diabetes == 1 else "No"),
        ]

        filas_html = "".join(f"""
            <tr style="background:{'#F4F8FB' if i % 2 == 0 else 'white'};">
                <td style="padding:7px 12px; color:#555; font-size:0.83rem;">{k}</td>
                <td style="padding:7px 12px; color:#1D3557; font-weight:600;
                        font-size:0.83rem; text-align:right;">{v}</td>
            </tr>""" for i, (k, v) in enumerate(resumen))

        st.markdown(f"""
        <div style="border-radius:6px; background:white; overflow:hidden;">
            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr style="background:#1D3557;">
                        <th style="padding:6px 12px; color:#ffffff; font-size:0.78rem;
                                font-weight:600; text-align:center;">Variable</th>
                        <th style="padding:6px 12px; color:#ffffff; font-size:0.78rem;
                                font-weight:600; text-align:center;">Valor</th>
                    </tr>
                </thead>
                <tbody>{filas_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col_detalle:
        st.markdown("""
        <div style="background:#EEF6FA; border-left:5px solid #0088AD;
                    border-radius:6px; padding:14px 18px; margin-bottom:14px;">
            <p style="margin:0; color:#1D3557; font-size:0.9rem; font-weight:600;">
                Resultado de la Clasificación
            </p>
        </div>
        """, unsafe_allow_html=True)

        if predecir_btn:
            datos_usuario = {
                "SEXO":                      sexo,
                "EDAD":                      edad,
                "PESO":                      peso,
                "TALLA":                     talla,
                "IMC":                       imc,
                "CATEGORIA_IMC":             cat_imc,
                "COLESTEROL_HDL":            col_hdl,
                "COLESTEROL_LDL":            col_ldl,
                "TRIGLICERIDOS":             trigli,
                "COLESTEROL_TOTAL":          col_total,
                "CREATININA_SERICA":         creat,
                "HABITO_TABAQUICO":          tabaquismo,
                "DIABETES":                  diabetes,
                "PRESION_ARTERIAL_SISTOLICA":  pas,
                "PRESION_ARTERIAL_DIASTOLICA": pad,
            }

            fila   = preparar_fila(datos_usuario, feature_names)
            fila_s = scaler.transform(fila)

            pred_num   = modelo.predict(fila_s)[0]
            pred_proba = modelo.predict_proba(fila_s)[0]
            pred_clase = le.inverse_transform([pred_num])[0]

            color, icono = color_riesgo(pred_clase)

            st.markdown(
                f"""
                <div style="
                    background:{color}22;
                    border: 2px solid {color};
                    border-radius: 12px;
                    padding: 12px 20px;
                    text-align: center;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 20px;
                ">
                    <span style="font-size:1.8rem;">{icono}</span>
                    <div>
                        <p style="font-size:0.82rem; color:gray; margin:0">Clasificación de riesgo</p>
                        <p style="font-size:1.6rem; font-weight:700; color:{color}; margin:0">
                            {pred_clase}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background:#EEF6FA; border-left:5px solid #0088AD;
                        border-radius:6px; padding:14px 18px; margin-bottom:14px;">
                <p style="margin:0; color:#1D3557; font-size:0.9rem; font-weight:600;">
                    Probabilidades por clase
                </p>
            </div>
            """, unsafe_allow_html=True)

            proba_df = pd.DataFrame(
                {"Clase": le.classes_, "Probabilidad (%)": (pred_proba * 100).round(2)}
            ).sort_values("Probabilidad (%)", ascending=False)

            for _, row in proba_df.iterrows():
                c, p = row["Clase"], row["Probabilidad (%)"]
                c_hex, _ = color_riesgo(c)
                ancho = int(p)
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
                        <span style="font-size:0.83rem; font-weight:600; color:#1D3557;">{c}</span>
                        <span style="font-size:0.83rem; font-weight:700; color:{c_hex};">{p:.1f}%</span>
                    </div>
                    <div style="background:#E8ECF0; border-radius:20px;
                                height:10px; overflow:hidden;">
                        <div style="width:{ancho}%; background:{c_hex};
                                    height:10px; border-radius:20px;
                                    transition: width 0.5s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
            <div style="background:#EEF6FA; border-left:5px solid #0088AD;
                        border-radius:6px; padding:14px 18px; margin-bottom:14px;">
                <p style="margin:0; color:#1D3557; font-size:0.9rem; font-weight:600;">
                    🔍 Variables más influyentes
                </p>
            </div>
            """, unsafe_allow_html=True)

            nombres_legibles = {
                "PRESION_ARTERIAL_SISTOLICA":  "Presión Sistólica",
                "PRESION_ARTERIAL_DIASTOLICA": "Presión Diastólica",
                "COLESTEROL_LDL":              "Colesterol LDL",
                "COLESTEROL_HDL":              "Colesterol HDL",
                "TRIGLICERIDOS":               "Triglicéridos",
                "COLESTEROL_TOTAL":            "Colesterol Total",
                "CREATININA_SERICA":           "Creatinina Sérica",
                "EDAD":                        "Edad",
                "IMC":                         "IMC",
                "PESO":                        "Peso",
                "TALLA":                       "Talla",
                "DIABETES":                    "Diabetes",
                "HABITO_TABAQUICO":            "Hábito Tabáquico",
                "SEXO":                        "Sexo",
            }

            importancias = pd.Series(
                modelo.feature_importances_, index=feature_names
            ).nlargest(5).sort_values(ascending=False)

            for var, val in importancias.items():
                nombre = nombres_legibles.get(var, var)
                ancho  = int(val * 100)
                porcentaje = round(val * 100, 1)
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between;
                                margin-bottom:3px;">
                        <span style="font-size:0.80rem; color:#555;">{nombre}</span>
                        <span style="font-size:0.80rem; font-weight:600; color:#0088AD;">{porcentaje}%</span>
                    </div>
                    <div style="background:#E8ECF0; border-radius:20px;
                                height:8px; overflow:hidden;">
                        <div style="width:{ancho}%; background:#0088AD;
                                    height:8px; border-radius:20px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("⬅️ Completa los datos en el panel lateral y presiona **Predecir riesgo**.")

    # ── Pie de página ─────────────────────────
    st.divider()
    st.caption(
        "⚠️ Esta herramienta es un apoyo computacional. "
        "No reemplaza el diagnóstico clínico de un profesional de la salud."
    )


if __name__ == "__main__":
    main()