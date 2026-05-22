"""
train.py — Entrenamiento del modelo Random Forest usando datos de la capa Gold.
Uso: python src/train.py
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, recall_score, make_scorer
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import argparse


GOLD_DIR   = os.path.join(os.path.dirname(__file__), '..', 'layers', 'gold')
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

TARGET = 'CLASIFICACION_RIESGO'


def recall_clase_alto(y_true, y_pred):
    return recall_score(y_true, y_pred, labels=[0], average='macro')


def entrenar(n_iter: int = 30):
    # Cargar dataset Gold
    ruta = os.path.join(GOLD_DIR, 'rcv_model_ready.csv')
    df   = pd.read_csv(ruta)
    print(f"✔ [TRAIN] Dataset Gold cargado: {df.shape[0]} filas, {df.shape[1]-1} features")

    X = df.drop(columns=[TARGET]).values
    y = df[TARGET].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"✔ [TRAIN] Train: {X_train.shape} | Test: {X_test.shape}")

    # Optimización de hiperparámetros
    scorer_alto = make_scorer(recall_clase_alto)
    grid_rf = {
        'n_estimators':     [100, 200, 300, 500],
        'max_depth':        [None, 5, 10, 20, 30],
        'min_samples_split':[2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features':     ['sqrt', 'log2'],
        'class_weight':     [None, 'balanced']
    }

    random_search = RandomizedSearchCV(
        estimator=RandomForestClassifier(random_state=42),
        param_distributions=grid_rf,
        n_iter=n_iter,
        scoring=scorer_alto,
        cv=5,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    random_search.fit(X_train, y_train)
    modelo = random_search.best_estimator_

    print("\n✔ Mejores hiperparámetros:")
    print(random_search.best_params_)
    print(f"\n✔ Mejor Recall clase ALTO: {random_search.best_score_:.4f}")

    # Evaluación
    y_pred = modelo.predict(X_test)
    le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.joblib'))

    print("\n══════════════════════════════")
    print("REPORTE DE CLASIFICACIÓN RF")
    print("══════════════════════════════")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    print("\nMATRIZ DE CONFUSIÓN RF")
    print("══════════════════════════════")
    print(confusion_matrix(y_test, y_pred))

    # Guardar modelo
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(modelo, os.path.join(MODELS_DIR, 'modelo_rf.joblib'))
    print(f"\n✔ [TRAIN] Modelo guardado en: {MODELS_DIR}/modelo_rf.joblib")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Entrenamiento RF - Riesgo Cardiovascular')
    parser.add_argument('--n_iter', type=int, default=30, help='Iteraciones RandomizedSearchCV')
    args = parser.parse_args()
    entrenar(n_iter=args.n_iter)
