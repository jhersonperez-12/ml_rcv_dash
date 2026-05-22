"""
pages/1_Dashboard.py — Dashboard de Storytelling
Riesgo Cardiovascular en Población Hipertensa
Diplomado en Ingeniería y Ciencia de Datos Aplicada · Unicomfacauca
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ──────────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard RCV · Storytelling",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR   = os.path.dirname(os.path.dirname(__file__))
SILVER_CSV = os.path.join(BASE_DIR, "layers", "silver", "rcv_clean.csv")
DATA_EXCEL = os.path.join(BASE_DIR, "data", "Clasificacion_RCV_Completo.xlsx")
MODELS_DIR = os.path.join(BASE_DIR, "models")

COLORES = {
    "ALTO":     "#E63946",
    "MODERADO": "#F4A261",
    "BAJO":     "#2DC653",
    "primario": "#1D3557",
    "fondo":    "#F8F9FA",
}

# ──────────────────────────────────────────────
# CARGA DE DATOS Y MODELO
# ──────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    # Intenta cargar el CSV procesado (entorno local con pipeline ejecutado)
    if os.path.exists(SILVER_CSV):
        df = pd.read_csv(SILVER_CSV)
    # Si no existe (Streamlit Cloud), procesa desde el Excel directamente
    elif os.path.exists(DATA_EXCEL):
        df = pd.read_excel(DATA_EXCEL)
        # Reemplazar códigos de ausencia por NaN
        codigos_ausencia = [99, 999, 9999]
        for col in df.select_dtypes(include="number").columns:
            df[col] = df[col].replace(codigos_ausencia, np.nan)
        # Imputar con mediana
        for col in df.select_dtypes(include="number").columns:
            df[col] = df[col].fillna(df[col].median())
    else:
        st.error("⚠️ No se encontró el archivo de datos. Sube 'data/Clasificacion_RCV_Completo.xlsx' al repositorio.")
        st.stop()

    df["SEXO_LABEL"] = df["SEXO"].map({1: "Masculino", 2: "Femenino"})
    df["DIABETES_LABEL"] = df["DIABETES"].map({0: "No", 1: "Sí"})
    df["TABAQUISMO_LABEL"] = df["HABITO_TABAQUICO"].map({
        0: "No fumador", 1: "Ex fumador",
        2: "Ocasional",  3: "Habitual"
    })
    bins   = [0, 40, 50, 60, 70, 80, 200]
    labels = ["<40", "40-49", "50-59", "60-69", "70-79", "80+"]
    df["GRUPO_EDAD"] = pd.cut(df["EDAD"], bins=bins, labels=labels, right=False)
    return df

@st.cache_resource
def cargar_modelo():
    modelo = joblib.load(os.path.join(MODELS_DIR, "modelo_rf.joblib"))
    with open(os.path.join(MODELS_DIR, "feature_names.json")) as f:
        features = json.load(f)
    return modelo, features

df = cargar_datos()
modelo, feature_names = cargar_modelo()

ORDEN_RIESGO  = ["ALTO", "MODERADO", "BAJO"]
COLOR_MAP     = {k: COLORES[k] for k in ORDEN_RIESGO}

# ──────────────────────────────────────────────
# ESTILOS CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .titulo-seccion {
        font-size: 1.35rem; font-weight: 700;
        color: #1D3557; border-left: 5px solid #E63946;
        padding-left: 12px; margin: 8px 0 4px 0;
    }
    .narrativa {
        background: #EEF2FF; border-radius: 10px;
        padding: 14px 18px; font-size: 0.97rem;
        color: #2C3E50; margin-bottom: 10px;
        border-left: 4px solid #1D3557;
    }
    .kpi-box {
        background: white; border-radius: 12px;
        padding: 18px 14px; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .kpi-valor { font-size: 2.2rem; font-weight: 800; margin: 0; }
    .kpi-label { font-size: 0.82rem; color: #666; margin: 0; }
    .seccion-divider {
        border: none; border-top: 2px solid #E8ECEF;
        margin: 28px 0 18px 0;
    }
    [data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ENCABEZADO
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{COLORES['primario']} 0%,#457B9D 100%);
            border-radius:14px; padding:28px 32px; margin-bottom:20px; color:white;">
    <h1 style="margin:0; font-size:1.9rem;">🫀 Estratificación del Riesgo Cardiovascular</h1>
    <p style="margin:6px 0 0 0; font-size:1rem; opacity:0.88;">
        Análisis de 5.000 pacientes hipertensos · EPS Colombia · Diplomado Ciencia de Datos · Unicomfacauca
    </p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SECCIÓN 1 — EL PROBLEMA
# ──────────────────────────────────────────────
st.markdown('<p class="titulo-seccion">📌 Sección 1 — El problema: un riesgo que los datos pueden anticipar</p>', unsafe_allow_html=True)
st.markdown("""
<div class="narrativa">
Las enfermedades cardiovasculares representan el <b>28% de las muertes en Colombia</b>.
Las EPS gestionan miles de pacientes hipertensos, pero la estratificación del riesgo se hace
de forma individual en consulta, sin aprovechar los datos clínicos disponibles.
Este proyecto demuestra que con las variables clínicas ya reportadas bajo la <b>Resolución 202 de 2021</b>,
es posible clasificar automáticamente el riesgo de cada afiliado y priorizar intervenciones preventivas.
</div>
""", unsafe_allow_html=True)

total        = len(df)
alto         = (df["CLASIFICACION_RIESGO"] == "ALTO").sum()
moderado     = (df["CLASIFICACION_RIESGO"] == "MODERADO").sum()
bajo         = (df["CLASIFICACION_RIESGO"] == "BAJO").sum()
pct_alto     = round(alto / total * 100, 1)

k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, f"{total:,}",    "Pacientes analizados",        COLORES["primario"]),
    (k2, f"{alto:,}",     "🔴 Riesgo ALTO",              COLORES["ALTO"]),
    (k3, f"{moderado:,}", "🟠 Riesgo MODERADO",          COLORES["MODERADO"]),
    (k4, f"{bajo:,}",     "🟢 Riesgo BAJO",              COLORES["BAJO"]),
    (k5, f"{pct_alto}%",  "Del total en riesgo crítico", COLORES["ALTO"]),
]
for col, val, lbl, color in kpis:
    col.markdown(f"""
    <div class="kpi-box">
        <p class="kpi-valor" style="color:{color}">{val}</p>
        <p class="kpi-label">{lbl}</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="seccion-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SECCIÓN 2 — CARACTERIZACIÓN DE LA POBLACIÓN
# ──────────────────────────────────────────────
st.markdown('<p class="titulo-seccion">👥 Sección 2 — ¿Quiénes son los pacientes?</p>', unsafe_allow_html=True)
st.markdown("""
<div class="narrativa">
La población analizada está conformada principalmente por mujeres mayores de 50 años,
con una marcada concentración en el grupo de 60 a 79 años.
Este perfil demográfico es coherente con la epidemiología de la hipertensión arterial,
cuya prevalencia aumenta con la edad y es más frecuente en mujeres después de la menopausia.
Entender quiénes son los pacientes es el primer paso para diseñar intervenciones efectivas.
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    sexo_df = df["SEXO_LABEL"].value_counts().reset_index()
    sexo_df.columns = ["Sexo", "Cantidad"]
    fig = px.pie(sexo_df, names="Sexo", values="Cantidad",
                 color_discrete_sequence=["#457B9D", "#E63946"],
                 title="Distribución por sexo", hole=0.45)
    fig.update_traces(textposition="outside", textinfo="percent+label")
    fig.update_layout(showlegend=False, margin=dict(t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    edad_df = df["GRUPO_EDAD"].value_counts().sort_index().reset_index()
    edad_df.columns = ["Grupo edad", "Pacientes"]
    fig = px.bar(edad_df, x="Grupo edad", y="Pacientes",
                 color="Pacientes", color_continuous_scale="Blues",
                 title="Distribución por grupo de edad")
    fig.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

with c3:
    imc_df = df["CATEGORIA_IMC"].value_counts().reset_index()
    imc_df.columns = ["Categoría IMC", "Pacientes"]
    fig = px.bar(imc_df, x="Categoría IMC", y="Pacientes",
                 color="Categoría IMC",
                 color_discrete_sequence=px.colors.qualitative.Safe,
                 title="Distribución por categoría IMC")
    fig.update_layout(showlegend=False, margin=dict(t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

# Distribución de riesgo por sexo
riesgo_sexo = df.groupby(["SEXO_LABEL", "CLASIFICACION_RIESGO"]).size().reset_index(name="n")
fig = px.bar(riesgo_sexo, x="SEXO_LABEL", y="n", color="CLASIFICACION_RIESGO",
             barmode="group", color_discrete_map=COLOR_MAP,
             category_orders={"CLASIFICACION_RIESGO": ORDEN_RIESGO},
             labels={"SEXO_LABEL": "Sexo", "n": "Pacientes", "CLASIFICACION_RIESGO": "Nivel de riesgo"},
             title="Nivel de riesgo cardiovascular por sexo")
fig.update_layout(margin=dict(t=40, b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<hr class="seccion-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SECCIÓN 3 — VARIABLES CLÍNICAS
# ──────────────────────────────────────────────
st.markdown('<p class="titulo-seccion">🔬 Sección 3 — ¿Qué dicen los datos clínicos?</p>', unsafe_allow_html=True)
st.markdown("""
<div class="narrativa">
Las variables clínicas muestran diferencias sistemáticas entre niveles de riesgo.
Los pacientes de riesgo ALTO presentan presiones arteriales más elevadas, mayores triglicéridos
y colesterol LDL más alto, mientras que el colesterol HDL (el "bueno") tiende a ser menor.
Estas diferencias son la base sobre la cual el modelo de clasificación aprende a distinguir los grupos.
</div>
""", unsafe_allow_html=True)

vars_clinicas = [
    ("PRESION_ARTERIAL_SISTOLICA", "Presión Sistólica (mmHg)"),
    ("PRESION_ARTERIAL_DIASTOLICA", "Presión Diastólica (mmHg)"),
    ("COLESTEROL_LDL", "Colesterol LDL (mg/dL)"),
    ("COLESTEROL_HDL", "Colesterol HDL (mg/dL)"),
    ("TRIGLICERIDOS", "Triglicéridos (mg/dL)"),
    ("IMC", "IMC (kg/m²)"),
]

col_a, col_b = st.columns(2)
for i, (var, label) in enumerate(vars_clinicas):
    fig = px.box(df, x="CLASIFICACION_RIESGO", y=var,
                 color="CLASIFICACION_RIESGO",
                 color_discrete_map=COLOR_MAP,
                 category_orders={"CLASIFICACION_RIESGO": ORDEN_RIESGO},
                 labels={"CLASIFICACION_RIESGO": "Nivel de riesgo", var: label},
                 title=f"{label} por nivel de riesgo")
    fig.update_layout(showlegend=False, margin=dict(t=40, b=10))
    if i % 2 == 0:
        col_a.plotly_chart(fig, use_container_width=True)
    else:
        col_b.plotly_chart(fig, use_container_width=True)

# Correlación
st.markdown("**Matriz de correlación entre variables clínicas**")
vars_corr = ["EDAD", "IMC", "COLESTEROL_HDL", "COLESTEROL_LDL",
             "TRIGLICERIDOS", "COLESTEROL_TOTAL", "CREATININA_SERICA",
             "PRESION_ARTERIAL_SISTOLICA", "PRESION_ARTERIAL_DIASTOLICA"]
corr = df[vars_corr].corr().round(2)
fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1, aspect="auto",
                title="Correlación entre variables clínicas y antropométricas")
fig.update_layout(margin=dict(t=40, b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<hr class="seccion-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SECCIÓN 4 — ARQUITECTURA MEDALLÓN
# ──────────────────────────────────────────────
st.markdown('<p class="titulo-seccion">🏗️ Sección 4 — De los datos crudos al dato analítico: Arquitectura Medallón</p>', unsafe_allow_html=True)
st.markdown("""
<div class="narrativa">
Los datos clínicos provenientes de la EPS presentaban valores inválidos (códigos 99, 999, 9999),
valores atípicos y variables categóricas sin codificar.
La arquitectura Medallón organizó el procesamiento en tres capas progresivas,
garantizando trazabilidad completa y reproducibilidad del pipeline de datos.
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
capas = [
    (m1, "🔶 Capa Bronze", "#CD7F32",
     "Ingesta del dato original",
     ["5.000 registros cargados", "16 variables clínicas", "Datos sin modificar", "Formato CSV preservado"]),
    (m2, "⚪ Capa Silver", "#A8A9AD",
     "Limpieza y preprocesamiento",
     ["Valores 99/999/9999 → mediana", "Outliers tratados con IQR", "Capping percentil 99", "115 registros corregidos"]),
    (m3, "🥇 Capa Gold", "#FFD700",
     "Datos listos para el modelo",
     ["One-Hot Encoding aplicado", "StandardScaler estandarizado", "17 features finales", "Variable objetivo codificada"]),
]
for col, titulo, color, sub, items in capas:
    items_html = "".join(f"<li>{it}</li>" for it in items)
    col.markdown(f"""
    <div style="background:white; border-radius:12px; padding:18px;
                border-top:5px solid {color}; box-shadow:0 2px 8px rgba(0,0,0,0.08); height:100%;">
        <h4 style="color:{color}; margin:0 0 4px 0">{titulo}</h4>
        <p style="color:#666; font-size:0.85rem; margin:0 0 10px 0">{sub}</p>
        <ul style="font-size:0.88rem; padding-left:18px; margin:0; color:#333">{items_html}</ul>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="seccion-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SECCIÓN 5 — RESULTADOS DEL MODELO
# ──────────────────────────────────────────────
st.markdown('<p class="titulo-seccion">🤖 Sección 5 — El modelo y su impacto en la gestión del riesgo</p>', unsafe_allow_html=True)
st.markdown("""
<div class="narrativa">
Se evaluaron tres algoritmos de clasificación supervisada: Regresión Logística, Random Forest y XGBoost.
<b>Random Forest fue seleccionado</b> por ofrecer el mejor equilibrio entre las tres clases de riesgo,
superando el criterio mínimo de <b>recall 90% para la clase ALTO</b>.
Esto significa que de cada 100 pacientes con riesgo cardiovascular crítico real,
el modelo identifica correctamente a <b>94</b>, permitiendo a la EPS priorizar intervenciones
preventivas antes de que ocurran eventos de alto costo.
</div>
""", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)
metricas = [
    (r1, "88%",  "Accuracy global",          COLORES["primario"]),
    (r2, "94%",  "Recall clase ALTO",         COLORES["ALTO"]),
    (r3, "75%",  "Recall clase MODERADO",     COLORES["MODERADO"]),
    (r4, "89%",  "Recall clase BAJO",         COLORES["BAJO"]),
]
for col, val, lbl, color in metricas:
    col.markdown(f"""
    <div class="kpi-box">
        <p class="kpi-valor" style="color:{color}">{val}</p>
        <p class="kpi-label">{lbl}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
ca, cb = st.columns(2)

# Comparativa de modelos
with ca:
    comp_df = pd.DataFrame({
        "Modelo":          ["Reg. Logística", "Random Forest", "XGBoost",
                            "Reg. Logística", "Random Forest", "XGBoost",
                            "Reg. Logística", "Random Forest", "XGBoost"],
        "Clase":           ["ALTO"]*3 + ["MODERADO"]*3 + ["BAJO"]*3,
        "Recall (%)":      [89, 94, 99, 28, 75, 52, 87, 89, 88],
    })
    fig = px.bar(comp_df, x="Modelo", y="Recall (%)", color="Clase",
                 barmode="group", color_discrete_map=COLOR_MAP,
                 category_orders={"Clase": ORDEN_RIESGO},
                 title="Comparativa de Recall por clase — 3 modelos optimizados",
                 text_auto=True)
    fig.update_layout(margin=dict(t=40, b=10), yaxis_range=[0, 105])
    st.plotly_chart(fig, use_container_width=True)

# Importancia de variables
with cb:
    importancias = pd.Series(
        modelo.feature_importances_, index=feature_names
    ).nlargest(10).sort_values()
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
    imp_df = importancias.reset_index()
    imp_df.columns = ["Variable", "Importancia"]
    imp_df["Variable"] = imp_df["Variable"].map(lambda x: nombres_legibles.get(x, x))
    fig = px.bar(imp_df, x="Importancia", y="Variable", orientation="h",
                 color="Importancia", color_continuous_scale="Reds",
                 title="Variables más influyentes en la clasificación (Top 10)")
    fig.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

# Matriz de confusión
st.markdown("**Matriz de confusión — Random Forest optimizado**")
conf_matrix = np.array([[662, 13, 33], [27, 416, 24], [33, 50, 242]])
fig = px.imshow(
    conf_matrix,
    labels=dict(x="Predicho", y="Real", color="Pacientes"),
    x=ORDEN_RIESGO, y=ORDEN_RIESGO,
    color_continuous_scale="Blues",
    text_auto=True,
    title="Matriz de confusión · Verde diagonal = clasificaciones correctas"
)
fig.update_layout(margin=dict(t=40, b=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<hr class="seccion-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CIERRE
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{COLORES['primario']} 0%,#457B9D 100%);
            border-radius:14px; padding:22px 32px; color:white; text-align:center;">
    <h3 style="margin:0 0 8px 0">💡 Conclusión del análisis</h3>
    <p style="margin:0; font-size:0.97rem; opacity:0.92; max-width:800px; margin:0 auto;">
        El modelo Random Forest permite identificar correctamente al <b>94% de los pacientes con riesgo cardiovascular alto</b>,
        transformando datos clínicos ya disponibles en la EPS en una herramienta concreta de gestión preventiva.
        Anticipar el riesgo reduce hospitalizaciones, eventos de alto costo y fortalece la sostenibilidad financiera del sistema.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("⚠️ Este dashboard es un apoyo académico y computacional. No reemplaza el diagnóstico clínico de un profesional de la salud.")
