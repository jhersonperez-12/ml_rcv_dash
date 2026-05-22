"""
silver.py — Capa Silver: Limpieza, imputación y estandarización de datos.
Responsabilidad: tomar los datos crudos de Bronze, limpiarlos y guardarlos en layers/silver/.
Uso: python src/silver.py
"""

import os
import numpy as np
import pandas as pd


BRONZE_DIR = os.path.join(os.path.dirname(__file__), '..', 'layers', 'bronze')
SILVER_DIR = os.path.join(os.path.dirname(__file__), '..', 'layers', 'silver')

VALORES_INVALIDOS = [99999, 999, 9999, 99]
COLUMNAS_IQR      = ['PESO', 'TALLA', 'EDAD', 'IMC']


def limpiar_invalidos(df: pd.DataFrame) -> pd.DataFrame:
    df.replace(VALORES_INVALIDOS, np.nan, inplace=True)
    return df


def imputar_mediana(df: pd.DataFrame) -> pd.DataFrame:
    numericas = df.select_dtypes(include=[np.number]).columns
    for col in numericas:
        if col.startswith('_'):   # no tocar metadatos de ingesta
            continue
        df[col].fillna(df[col].median(), inplace=True)
    return df


def capar_iqr(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    Q1, Q3 = df[columna].quantile(0.25), df[columna].quantile(0.75)
    IQR = Q3 - Q1
    df[columna] = np.clip(df[columna], Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
    return df


def tratar_outliers(df: pd.DataFrame) -> pd.DataFrame:
    for col in COLUMNAS_IQR:
        if col in df.columns:
            df = capar_iqr(df, col)

    if 'COLESTEROL_HDL' in df.columns:
        df['COLESTEROL_HDL'] = np.clip(df['COLESTEROL_HDL'], 20, None)

    if 'COLESTEROL_LDL' in df.columns:
        mediana_ldl = df[df['COLESTEROL_LDL'] >= 20]['COLESTEROL_LDL'].median()
        df.loc[df['COLESTEROL_LDL'] < 20, 'COLESTEROL_LDL'] = mediana_ldl

    if 'TRIGLICERIDOS' in df.columns:
        df['TRIGLICERIDOS'] = np.clip(df['TRIGLICERIDOS'], None, df['TRIGLICERIDOS'].quantile(0.99))

    if 'CREATININA_SERICA' in df.columns:
        df['CREATININA_SERICA'] = np.clip(df['CREATININA_SERICA'], None, df['CREATININA_SERICA'].quantile(0.99))

    return df


def procesar() -> str:
    os.makedirs(SILVER_DIR, exist_ok=True)

    entrada = os.path.join(BRONZE_DIR, 'rcv_raw.csv')
    df = pd.read_csv(entrada)
    print(f"✔ [SILVER] Datos leídos desde Bronze: {df.shape[0]} filas")

    df = limpiar_invalidos(df)
    df = imputar_mediana(df)
    df = tratar_outliers(df)

    # Eliminar columnas de metadatos de ingesta antes de guardar
    df.drop(columns=[c for c in df.columns if c.startswith('_')], inplace=True, errors='ignore')

    salida = os.path.join(SILVER_DIR, 'rcv_clean.csv')
    df.to_csv(salida, index=False)
    print(f"✔ [SILVER] Datos limpios guardados en: {salida}")
    return salida


if __name__ == '__main__':
    procesar()
