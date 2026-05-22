# ❤️ Clasificador de Riesgo Cardiovascular — Arquitectura Medallón

Proyecto de Machine Learning para clasificación de riesgo cardiovascular usando **Random Forest**,
estructurado bajo la **Arquitectura Medallón** (Bronze → Silver → Gold).

## Estructura del proyecto

```
rcv_medallon/
├── pipeline.py             # Orquestador: ejecuta todo el pipeline de una vez
├── app.py                  # Aplicación Streamlit para predicción
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── bronze.py           # 🔶 Capa Bronze: ingesta de datos crudos
│   ├── silver.py           # ⚪ Capa Silver: limpieza y preprocesamiento
│   ├── gold.py             # 🥇 Capa Gold:  encoding, escalado, dataset final
│   └── train.py            # 🤖 Entrenamiento del modelo Random Forest
│
├── layers/                 # Generado automáticamente al correr el pipeline
│   ├── bronze/
│   │   └── rcv_raw.csv         ← datos crudos + metadatos de ingesta
│   ├── silver/
│   │   └── rcv_clean.csv       ← datos limpios sin outliers
│   └── gold/
│       └── rcv_model_ready.csv ← dataset escalado y codificado
│
├── models/                 # Artefactos del modelo (generados al entrenar)
│   ├── modelo_rf.joblib
│   ├── scaler.joblib
│   ├── label_encoder.joblib
│   └── feature_names.json
│
└── data/
    └── Clasificacion_RCV_Completo.xlsx   ← coloca aquí tu archivo
```

## ¿Qué hace cada capa?

| Capa       | Archivo        | Responsabilidad                                              |
|------------|----------------|--------------------------------------------------------------|
| 🔶 Bronze  | `bronze.py`    | Lee el Excel original sin modificarlo. Agrega metadatos de ingesta (fecha, fuente). |
| ⚪ Silver  | `silver.py`    | Limpia valores inválidos, imputa medianas, corrige outliers.  |
| 🥇 Gold    | `gold.py`      | Aplica one-hot encoding, StandardScaler. Genera el dataset listo para modelar. |
| 🤖 Train   | `train.py`     | Entrena el Random Forest con RandomizedSearchCV sobre los datos Gold. |

## Instalación

```bash
pip install -r requirements.txt
```

## Paso 1 — Ejecutar el pipeline completo

```bash
python pipeline.py --data data/Clasificacion_RCV_Completo.xlsx
```

Para una prueba rápida con menos iteraciones:

```bash
python pipeline.py --data data/Clasificacion_RCV_Completo.xlsx --n_iter 10
```

También puedes ejecutar cada capa por separado:

```bash
python src/bronze.py --data data/Clasificacion_RCV_Completo.xlsx
python src/silver.py
python src/gold.py
python src/train.py
```

## Paso 2 — Lanzar la aplicación

```bash
python -m streamlit run app.py
```

La app abre en `http://localhost:8501`.

## Despliegue en Streamlit Cloud

1. Sube el proyecto a GitHub (sin la carpeta `data/` ni `layers/`)
2. Entra a **share.streamlit.io**
3. Conecta tu repositorio
4. **Main file path:** `app.py`
5. Click en **Deploy**

> ⚠️ Los archivos `.joblib` deben estar en `models/` antes de desplegar,
> ya que Streamlit Cloud no ejecuta el pipeline de entrenamiento automáticamente.
