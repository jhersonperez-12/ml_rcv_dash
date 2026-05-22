"""
pipeline.py — Orquestador del pipeline completo Medallón.
Ejecuta las 4 etapas en secuencia: Bronze → Silver → Gold → Train
Uso: python pipeline.py --data data/Clasificacion_RCV_Completo.xlsx
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import bronze
import silver
import gold
import train


def ejecutar_pipeline(ruta_data: str, n_iter: int = 30):
    print("\n" + "="*50)
    print("  PIPELINE MEDALLÓN — RIESGO CARDIOVASCULAR")
    print("="*50)

    print("\n🔶 CAPA BRONZE — Ingesta de datos crudos")
    print("-"*40)
    bronze.ingestar(ruta_data)

    print("\n⚪ CAPA SILVER — Limpieza y preprocesamiento")
    print("-"*40)
    silver.procesar()

    print("\n🥇 CAPA GOLD   — Encoding y escalado")
    print("-"*40)
    gold.procesar()

    print("\n🤖 ENTRENAMIENTO — Random Forest")
    print("-"*40)
    train.entrenar(n_iter=n_iter)

    print("\n" + "="*50)
    print("  ✔ PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*50 + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pipeline Medallón - Riesgo Cardiovascular')
    parser.add_argument('--data',   type=str, required=True, help='Ruta al archivo Excel')
    parser.add_argument('--n_iter', type=int, default=30,    help='Iteraciones RandomizedSearchCV')
    args = parser.parse_args()
    ejecutar_pipeline(args.data, args.n_iter)
