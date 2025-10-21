import re
from pathlib import Path
from typing import List

import emoji
import joblib
import spacy

# --- Carga única de modelos al iniciar Django ---

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "ml_model" / "ml_modelo_emociones.pkl"
VECTORIZER_PATH = BASE_DIR / "ml_model" / "ml_vectorizador_tfidf.pkl"

try:
    # Cargar los objetos una sola vez
    nlp = spacy.load("es_core_news_md")
    modelo_cargado = joblib.load(MODEL_PATH)
    vectorizador_cargado = joblib.load(VECTORIZER_PATH)
    nombres_emociones = ["alegria", "tristeza", "ira", "miedo", "sorpresa", "asco"]
    print("✅ Modelos de ML cargados correctamente.")
except FileNotFoundError:
    print("❌ Error: No se encontraron los archivos del modelo. Asegúrate de que están en diary/ml_model/")
    nlp = None
    modelo_cargado = None
    vectorizador_cargado = None

# --- Funciones de preprocesamiento (las mismas que usaste para entrenar) ---


def preprocesar_texto(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = emoji.demojize(texto, language="es")
    texto = re.sub(r"https?://\S+|www\.\S+", "", texto)
    texto = re.sub(r"@\w+", "", texto)
    texto = re.sub(r"#\w+", "", texto)
    texto = re.sub(r"(.)\1{2,}", r"\1", texto)
    texto = re.sub(r"([,.!?])", r" \1 ", texto)
    texto = re.sub(r"[^a-záéíóúüñ_.,!?:]", " ", texto)
    texto = re.sub(r"\s{2,}", " ", texto).strip()
    return texto


def lematizar_texto(texto: str) -> List[str]:
    doc = nlp(texto)
    return [token.lemma_ for token in doc if token.text.strip()]


# --- Función principal del servicio ---


def analizar_emociones_texto(texto: str) -> List[str]:
    """
    Toma un texto, lo procesa y devuelve una lista de emociones predichas.
    """
    if not all([modelo_cargado, vectorizador_cargado, nlp]):
        return ["Error en el servicio de ML"]

    texto_procesado = " ".join(lematizar_texto(preprocesar_texto(texto)))
    texto_vectorizado = vectorizador_cargado.transform([texto_procesado])
    prediccion = modelo_cargado.predict(texto_vectorizado)

    emociones_predichas = [nombres_emociones[i] for i, valor in enumerate(prediccion[0]) if valor == 1]

    return emociones_predichas
