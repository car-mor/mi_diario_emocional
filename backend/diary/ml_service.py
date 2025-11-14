"""
Módulo de predicción de emociones con modelo BETO fine-tuneado
Compatible con el modelo entrenado en el notebook mejorado
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

import emoji
import spacy
import torch
from decouple import config
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
MODEL_ID = config("EMOTION_MODEL_ID", default="c-armor/finetuned_emotions")
HF_TOKEN = config("HF_TOKEN", default=None)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EMOTION_LABELS = ["alegria", "tristeza", "ira", "miedo", "sorpresa", "asco"]

UMBRALES = {
    "alegria": 0.50,
    "tristeza": 0.50,
    "ira": 0.50,
    "miedo": 0.30,
    "sorpresa": 0.30,
    "asco": 0.35,
}

# ============================================================
# VARIABLES GLOBALES (inicialmente None)
# ============================================================
_NLP = None
_TOKENIZER = None
_MODEL = None

# ============================================================
# FUNCIONES DE CARGA LAZY (solo cuando se necesiten)
# ============================================================


def get_spacy_model():
    """Carga spaCy solo cuando se necesita (lazy loading)"""
    global _NLP
    if _NLP is None:
        print("🔄 Cargando modelo spaCy...")
        _NLP = spacy.load("es_core_news_md")
        print("✅ spaCy cargado")
    return _NLP


def get_transformer_models():
    """Carga BETO solo cuando se necesita (lazy loading)"""
    global _TOKENIZER, _MODEL
    if _TOKENIZER is None or _MODEL is None:
        print(f"🔄 Cargando modelo BETO desde {MODEL_ID} en dispositivo: {DEVICE}...")
        try:
            _TOKENIZER = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
            _MODEL = AutoModelForSequenceClassification.from_pretrained(MODEL_ID, token=HF_TOKEN)
            _MODEL.to(DEVICE)
            _MODEL.eval()
            print(f"✅ BETO cargado exitosamente en {DEVICE}")
        except Exception as e:
            print(f"❌ Error cargando BETO: {e}")
            print("\n📋 SOLUCIÓN:")
            print("   1. Verifica conexión a internet")
            print(f"   2. Verifica que el ID del modelo '{MODEL_ID}' sea correcto")
            raise
    return _TOKENIZER, _MODEL


# ============================================================
# FUNCIONES DE PREPROCESAMIENTO
# ============================================================


def preprocesar_texto(texto: str) -> str:
    """Limpia y normaliza el texto"""
    if not isinstance(texto, str):
        return ""

    texto = texto.lower()
    texto = emoji.demojize(texto, language="es")
    texto = re.sub(r"\bno\s+", "no_", texto)
    texto = re.sub(r"\bnunca\s+", "nunca_", texto)
    texto = re.sub(r"https?://\S+|www\.\S+", "", texto)
    texto = re.sub(r"@\w+", "", texto)
    texto = re.sub(r"#\w+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñ_.,!?¿¡]", " ", texto)
    texto = re.sub(r"\s{2,}", " ", texto).strip()

    return texto


def lematizar_texto_para_beto(texto: str) -> str:
    """Lematiza el texto y devuelve un STRING (para BETO)"""
    nlp = get_spacy_model()  # ✅ Carga bajo demanda

    with nlp.disable_pipes("parser", "ner"):
        doc = nlp(texto)

    return " ".join([token.lemma_ for token in doc if token.text.strip()])


def lematizar_texto_para_lista(texto: str) -> List[str]:
    """Lematiza el texto y devuelve una LISTA (para nube de palabras)"""
    nlp = get_spacy_model()  # ✅ Carga bajo demanda

    with nlp.disable_pipes("parser", "ner"):
        doc = nlp(texto)

    return [token.lemma_ for token in doc if token.text.strip()]


# ============================================================
# FUNCIÓN PRINCIPAL DE PREDICCIÓN
# ============================================================


def analizar_emociones_con_beto(texto: str) -> Tuple[List[str], Dict[str, float]]:
    """
    Predice emociones usando el modelo BETO fine-tuneado.

    Los modelos se cargan automáticamente la primera vez que se llama.
    """
    # Validar entrada
    if not texto or not isinstance(texto, str) or len(texto.strip()) < 3:
        return ["texto_invalido"], {}

    try:
        # Cargar modelos solo cuando se necesitan
        tokenizer, model = get_transformer_models()  # ✅ Carga bajo demanda

        # 1. Preprocesar y lematizar
        texto_limpio = preprocesar_texto(texto)
        texto_lematizado = lematizar_texto_para_beto(texto_limpio)

        # 2. Tokenizar para BETO
        inputs = tokenizer(texto_lematizado, padding=True, truncation=True, max_length=128, return_tensors="pt").to(
            DEVICE
        )

        # 3. Obtener predicciones
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        # 4. Convertir a probabilidades
        probabilidades = torch.sigmoid(logits).cpu().numpy()[0]

        # 5. Analizar cada emoción
        emociones_detectadas = []
        probabilidades_dict = {}

        for i, emocion in enumerate(EMOTION_LABELS):
            prob = float(probabilidades[i])
            umbral = UMBRALES[emocion]
            probabilidades_dict[emocion] = round(prob, 4)

            if prob >= umbral:
                emociones_detectadas.append(emocion)

        # 6. Si no se detectó ninguna emoción, marcar como neutro
        if not emociones_detectadas:
            emociones_detectadas = ["neutro"]

        return emociones_detectadas, probabilidades_dict

    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        return ["error_prediccion"], {}
