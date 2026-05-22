"""
bronze.py — Capa Bronze: Ingesta de datos crudos sin transformación.
Responsabilidad: leer el Excel original y guardarlo como CSV crudo en layers/bronze/.
Uso: python src/bronze.py --data data/Clasificacion_RCV_Completo.xlsx
"""

import argparse
import os
from datetime import datetime
import pandas as pd


BRONZE_DIR = os.path.join(os.path.dirname(__file__), '..', 'layers', 'bronze')


def ingestar(ruta_excel: str) -> str:
    os.makedirs(BRONZE_DIR, exist_ok=True)

    df = pd.read_excel(ruta_excel)
    print(f"✔ [BRONZE] Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")

    # Agregar metadatos de ingesta
    df['_ingesta_fecha'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['_ingesta_fuente'] = os.path.basename(ruta_excel)

    salida = os.path.join(BRONZE_DIR, 'rcv_raw.csv')
    df.to_csv(salida, index=False)
    print(f"✔ [BRONZE] Datos crudos guardados en: {salida}")
    return salida


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Capa Bronze - Ingesta de datos crudos')
    parser.add_argument('--data', type=str, required=True, help='Ruta al archivo Excel')
    args = parser.parse_args()
    ingestar(args.data)
