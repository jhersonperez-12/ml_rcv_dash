"""
gold.py — Capa Gold: Encoding, escalado y dataset listo para modelamiento.
Responsabilidad: tomar los datos limpios de Silver, aplicar transformaciones finales
y guardar el dataset listo para entrenar en layers/gold/.
Uso: python src/gold.py
"""

import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


SILVER_DIR = os.path.join(os.path.dirname(__file__), '..', 'layers', 'silver')
GOLD_DIR   = os.path.join(os.path.dirname(__file__), '..', 'layers', 'gold')
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

TARGET = 'CLASIFICACION_RIESGO'


def procesar() -> str:
    os.makedirs(GOLD_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)

    entrada = os.path.join(SILVER_DIR, 'rcv_clean.csv')
    df = pd.read_csv(entrada)
    print(f"✔ [GOLD] Datos leídos desde Silver: {df.shape[0]} filas")

    # One-hot encoding de variables categóricas (excepto target)
    categoricas = df.drop(columns=[TARGET]).select_dtypes(include=['object']).columns.tolist()
    df = pd.get_dummies(df, columns=categoricas, drop_first=True)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    # Encoding del target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Escalado
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Guardar dataset Gold como CSV
    df_gold = pd.DataFrame(X_scaled, columns=X.columns)
    df_gold[TARGET] = y_encoded
    salida = os.path.join(GOLD_DIR, 'rcv_model_ready.csv')
    df_gold.to_csv(salida, index=False)

    # Guardar artefactos de transformación
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.joblib'))
    joblib.dump(le,     os.path.join(MODELS_DIR, 'label_encoder.joblib'))
    with open(os.path.join(MODELS_DIR, 'feature_names.json'), 'w') as f:
        json.dump(X.columns.tolist(), f)

    print(f"✔ [GOLD] Dataset listo guardado en: {salida}")
    print(f"✔ [GOLD] Artefactos (scaler, encoder, features) guardados en: {MODELS_DIR}/")
    return salida


if __name__ == '__main__':
    procesar()
