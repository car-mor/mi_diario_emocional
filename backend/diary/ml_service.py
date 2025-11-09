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
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ============================================================
# CONFIGURACIÓN
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "ml_model"  # Carpeta donde descomprimiste el modelo
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EMOTION_LABELS = ["alegria", "tristeza", "ira", "miedo", "sorpresa", "asco"]

# ⭐ UMBRALES ACTUALIZADOS (los mismos del notebook mejorado)
UMBRALES = {
    "alegria": 0.50,
    "tristeza": 0.50,
    "ira": 0.50,
    "miedo": 0.30,    # Ajustado para clases raras
    "sorpresa": 0.30, # Ajustado para clases raras
    "asco": 0.35      # Ajustado para clases raras
}

# ============================================================
# CARGA DE MODELOS (Solo una vez al iniciar)
# ============================================================
try:
    print(f"🔄 Cargando modelos de ML en dispositivo: {DEVICE}...")
    
    # Verificar que la carpeta existe
    if not MODEL_DIR.exists():
        raise FileNotFoundError(
            f"❌ No se encontró la carpeta del modelo: {MODEL_DIR}\n"
            f"   Asegúrate de haber descargado y descomprimido el modelo."
        )
    
    # Cargar spaCy
    NLP = spacy.load("es_core_news_md")
    
    # Cargar BETO fine-tuneado
    TOKENIZER = AutoTokenizer.from_pretrained(MODEL_DIR)
    MODEL = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    MODEL.to(DEVICE)
    MODEL.eval()  # Modo evaluación (importante)
    
    print(f"✅ Modelos cargados exitosamente")
    print(f"   • spaCy: es_core_news_md")
    print(f"   • BETO fine-tuneado: {MODEL_DIR}")
    print(f"   • Dispositivo: {DEVICE}")
    
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("\n📋 SOLUCIÓN:")
    print("   1. Ejecuta en Colab el código de exportación")
    print("   2. Descarga 'modelo_finetuned_mejorado.zip'")
    print(f"   3. Descomprímelo en: {MODEL_DIR}")
    NLP, TOKENIZER, MODEL = None, None, None
    
except Exception as e:
    print(f"❌ Error crítico cargando modelos: {e}")
    NLP, TOKENIZER, MODEL = None, None, None


# ============================================================
# FUNCIONES DE PREPROCESAMIENTO
# ============================================================

def preprocesar_texto(texto: str) -> str:
    """
    Limpia y normaliza el texto (mismo proceso del notebook).
    """
    if not isinstance(texto, str):
        return ""
    
    texto = texto.lower()
    texto = emoji.demojize(texto, language="es")
    
    # Preservar negaciones
    texto = re.sub(r"\bno\s+", "no_", texto)
    texto = re.sub(r"\bnunca\s+", "nunca_", texto)
    
    # Eliminar URLs, menciones, hashtags
    texto = re.sub(r"https?://\S+|www\.\S+", "", texto)
    texto = re.sub(r"@\w+", "", texto)
    texto = re.sub(r"#\w+", "", texto)
    
    # Limpiar caracteres especiales (conservar puntuación emocional)
    texto = re.sub(r"[^a-záéíóúüñ_.,!?¿¡]", " ", texto)
    texto = re.sub(r"\s{2,}", " ", texto).strip()
    
    return texto


def lematizar_texto_para_beto(texto: str) -> str:
    """
    Lematiza el texto y devuelve un STRING (para BETO).
    """
    if not NLP:
        return texto  # Fallback si spaCy no cargó
    
    with NLP.disable_pipes("parser", "ner"):
        doc = NLP(texto)
    
    return " ".join([token.lemma_ for token in doc if token.text.strip()])


def lematizar_texto_para_lista(texto: str) -> List[str]:
    """
    Lematiza el texto y devuelve una LISTA (para nube de palabras).
    """
    if not NLP:
        return texto.split()  # Fallback
    
    with NLP.disable_pipes("parser", "ner"):
        doc = NLP(texto)
    
    return [token.lemma_ for token in doc if token.text.strip()]


# ============================================================
# FUNCIÓN PRINCIPAL DE PREDICCIÓN
# ============================================================

def analizar_emociones_con_beto(texto: str) -> Tuple[List[str], Dict[str, float]]:
    """
    Predice emociones usando el modelo BETO fine-tuneado.
    
    Args:
        texto (str): Texto a analizar
    
    Returns:
        Tuple[List[str], Dict[str, float]]: 
            - Lista de emociones detectadas (ej: ['miedo', 'sorpresa'])
            - Diccionario con probabilidades de todas las emociones
    
    Example:
        >>> emociones, probs = analizar_emociones_con_beto("Estoy muy feliz")
        >>> print(emociones)  # ['alegria']
        >>> print(probs)      # {'alegria': 0.8234, 'tristeza': 0.1234, ...}
    """
    
    # Verificar que los modelos estén cargados
    if not all([MODEL, TOKENIZER, NLP]):
        return ["error_modelo_no_cargado"], {}
    
    # Validar entrada
    if not texto or not isinstance(texto, str) or len(texto.strip()) < 3:
        return ["texto_invalido"], {}
    
    try:
        # 1. Preprocesar y lematizar
        texto_limpio = preprocesar_texto(texto)
        texto_lematizado = lematizar_texto_para_beto(texto_limpio)
        
        # 2. Tokenizar para BETO
        inputs = TOKENIZER(
            texto_lematizado,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        ).to(DEVICE)
        
        # 3. Obtener predicciones
        with torch.no_grad():
            outputs = MODEL(**inputs)
            logits = outputs.logits
        
        # 4. Convertir a probabilidades (sigmoid para multi-label)
        probabilidades = torch.sigmoid(logits).cpu().numpy()[0]
        
        # 5. Analizar cada emoción
        emociones_detectadas = []
        probabilidades_dict = {}
        
        for i, emocion in enumerate(EMOTION_LABELS):
            prob = float(probabilidades[i])
            umbral = UMBRALES[emocion]
            
            # Guardar probabilidad (redondeada a 4 decimales)
            probabilidades_dict[emocion] = round(prob, 4)
            
            # Detectar si supera el umbral
            if prob >= umbral:
                emociones_detectadas.append(emocion)
        
        # 6. Si no se detectó ninguna emoción, marcar como neutro
        if not emociones_detectadas:
            emociones_detectadas = ["neutro"]
        
        return emociones_detectadas, probabilidades_dict
    
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        return ["error_prediccion"], {}


# # ============================================================
# # FUNCIÓN DE DIAGNÓSTICO (Opcional)
# # ============================================================

# def diagnosticar_modelo() -> Dict[str, any]:
#     """
#     Verifica el estado del modelo y devuelve información de diagnóstico.
#     Útil para debugging.
#     """
#     diagnostico = {
#         "modelo_cargado": MODEL is not None,
#         "tokenizer_cargado": TOKENIZER is not None,
#         "spacy_cargado": NLP is not None,
#         "dispositivo": DEVICE,
#         "ruta_modelo": str(MODEL_DIR),
#         "modelo_existe": MODEL_DIR.exists(),
#         "emociones": EMOTION_LABELS,
#         "umbrales": UMBRALES
#     }
    
#     if MODEL:
#         diagnostico["num_parametros"] = sum(p.numel() for p in MODEL.parameters())
#         diagnostico["num_etiquetas"] = MODEL.config.num_labels
    
#     return diagnostico


# # ============================================================
# # FUNCIÓN DE PRUEBA (Para ejecutar directamente)
# # ============================================================

# if __name__ == "__main__":
#     print("\n" + "=" * 60)
#     print("🧪 PRUEBA DEL PREDICTOR")
#     print("=" * 60)
    
#     # Mostrar diagnóstico
#     diag = diagnosticar_modelo()
#     print("\n--- DIAGNÓSTICO ---")
#     for key, value in diag.items():
#         print(f"  • {key}: {value}")
    
#     # Textos de prueba
#     textos_prueba = [
#         "Estoy muy feliz por los resultados del proyecto",
#         "Tengo mucho miedo de salir de noche por esta zona",
#         "La reunión fue una pérdida de tiempo absoluta",
#         "¡Qué sorpresa tan agradable! No lo esperaba"
#     ]
    
#     print("\n--- PREDICCIONES ---")
#     for texto in textos_prueba:
#         print(f"\n📝 Texto: '{texto[:60]}...'")
#         emociones, probs = analizar_emociones_con_beto(texto)
        
#         print(f"   Emociones: {emociones}")
#         print(f"   Probabilidades:")
#         for emocion, prob in probs.items():
#             simbolo = "✓" if prob >= UMBRALES[emocion] else "✗"
#             print(f"      {simbolo} {emocion.capitalize():<10}: {prob:.4f}")
    
#     print("\n" + "=" * 60)