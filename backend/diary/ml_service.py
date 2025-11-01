import re
from pathlib import Path
from typing import Dict, List, Tuple

import emoji
import spacy
import torch

# from scipy.special import expit
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# --- 0. Definir rutas y nombres ---
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "ml_model"  # Apunta a la carpeta que renombraste
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EMOTION_LABELS = ["alegria", "tristeza", "ira", "miedo", "sorpresa", "asco"]

# Umbrales que definiste en tu notebook (Celda 12)
UMBRALES = {"alegria": 0.48, "tristeza": 0.50, "ira": 0.50, "miedo": 0.30, "sorpresa": 0.30, "asco": 0.35}

# --- 1. Cargar modelos (solo una vez) ---
try:
    print(f"Cargando modelos de ML en dispositivo: {DEVICE}...")
    NLP = spacy.load("es_core_news_md")
    TOKENIZER = AutoTokenizer.from_pretrained(MODEL_DIR)
    MODEL = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    MODEL.to(DEVICE)
    MODEL.eval()  # Poner el modelo en modo de evaluación
    print("✅ Modelos de emoción (fine-tuned) cargados.")
except Exception as e:
    print(f"❌ Error crítico cargando modelos: {e}")
    NLP, TOKENIZER, MODEL = None, None, None


# --- 2. Funciones de Preprocesamiento (las de tu notebook) ---
def preprocesar_texto(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = emoji.demojize(texto, language="es")
    texto = re.sub(r"\bno\s+", "no_", texto)
    texto = re.sub(r"\bnunca\s+", "nunca_", texto)
    texto = re.sub(r"https?://\S+|www\.\S+", "", texto)
    texto = re.sub(r"@\w+", "", texto)
    texto = re.sub(r"#\w+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñ_]", " ", texto)  # Tu versión simplificada
    texto = re.sub(r"\s{2,}", " ", texto).strip()
    return texto


# def lematizar_texto(texto: str) -> str:
#     # Devuelve un solo string, no una lista
#     with NLP.disable_pipes("parser", "ner"):
#         doc = NLP(texto)
#     return " ".join([token.lemma_ for token in doc if token.text.strip()])


def lematizar_texto_para_lista(texto: str) -> List[str]:
    """
    NUEVA FUNCIÓN: Devuelve una LISTA de lemmas para la nube de palabras.
    """
    with NLP.disable_pipes("parser", "ner"):
        doc = NLP(texto)
    return [token.lemma_ for token in doc if token.text.strip()]


def lematizar_texto_para_beto(texto: str) -> str:
    """
    FUNCIÓN ANTIGUA (RENOMBRADA): Devuelve un STRING para el modelo BETO.
    """
    with NLP.disable_pipes("parser", "ner"):
        doc = NLP(texto)
    return " ".join([token.lemma_ for token in doc if token.text.strip()])


# --- 3. Función de Predicción Principal ---
def analizar_emociones_con_beto(texto: str) -> Tuple[List[str], Dict[str, float]]:
    """
    Predice las emociones de un texto usando el modelo fine-tuneado.
    Devuelve las etiquetas detectadas y el diccionario de probabilidades.
    """
    if not all([MODEL, TOKENIZER, NLP]):
        return ["Error: Modelo no cargado"], {}

    # Preprocesar y lematizar
    texto_limpio = preprocesar_texto(texto)
    texto_lematizado = lematizar_texto_para_beto(texto_limpio)

    # Tokenizar
    inputs = TOKENIZER(texto_lematizado, padding=True, truncation=True, max_length=128, return_tensors="pt").to(DEVICE)

    # Predecir
    with torch.no_grad():
        outputs = MODEL(**inputs)
        logits = outputs.logits

    # Probabilidades
    probabilidades = torch.sigmoid(logits).cpu().numpy()[0]

    emociones_detectadas = []
    probabilidades_dict = {}

    for i, emocion in enumerate(EMOTION_LABELS):
        prob = probabilidades[i]
        umbral = UMBRALES[emocion]

        probabilidades_dict[emocion] = round(float(prob), 4)

        if prob >= umbral:
            emociones_detectadas.append(emocion)

    if not emociones_detectadas and probabilidades_dict:
        # Ordena el diccionario por probabilidad (valor) de mayor a menor
        sorted_emociones = sorted(probabilidades_dict.items(), key=lambda item: item[1], reverse=True)
        # Extrae los nombres de las dos emociones más altas
        emociones_detectadas = [emocion for emocion, prob in sorted_emociones[:2]]
        

    return emociones_detectadas, probabilidades_dict
