from typing import Dict, List, Tuple

from decouple import config
from gradio_client import Client

# --- 1. CONFIGURACIÓN A NIVEL DE MÓDULO ---
HF_SPACE_URL = config("HF_SPACE_URL")

print(f"🔄 Conectando al cliente de Gradio en: {HF_SPACE_URL}")
try:
    API_CLIENT = Client(HF_SPACE_URL)
    print("✅ Cliente de Gradio conectado y listo.")
except Exception as e:
    print(f"❌ ERROR CRÍTICO: No se pudo conectar al Gradio Space: {e}")
    API_CLIENT = None


# --- 3. FUNCIÓN DE PREDICCIÓN (Emociones) ---
def analizar_emociones_con_beto(texto: str) -> Tuple[List[str], Dict[str, float]]:
    if API_CLIENT is None:
        print("Error: API_CLIENT no está inicializado.")
        return ["error_api"], {}
    try:
        result = API_CLIENT.predict(
            texto,
            api_name="/predict_emotions",  # <-- Usa el api_name de emociones
        )
        emociones = result.get("emociones", ["error_parseo"])
        probabilidades = result.get("probabilidades", {})
        return emociones, probabilidades
    except Exception as e:
        print(f"❌ Error durante la predicción de emociones: {e}")
        return ["error_api"], {}


# --- 4. NUEVA FUNCIÓN DE PREDICCIÓN (Frecuencia) ---
def obtener_frecuencia_palabras(texto: str) -> List[List]:
    """
    Obtiene la frecuencia de palabras llamando a la API
    desplegada en Hugging Face Spaces.
    """
    if API_CLIENT is None:
        print("Error: API_CLIENT no está inicializado.")
        return []
    try:
        # Llama al nuevo endpoint de frecuencia
        result = API_CLIENT.predict(
            texto,
            api_name="/predict_frequency",  # <-- Usa el api_name de frecuencia
        )
        # 'result' ya es la lista de listas, ej: [["hola", 2], ["mundo", 1]]
        return result
    except Exception as e:
        print(f"❌ Error durante la predicción de frecuencia: {e}")
        return []
