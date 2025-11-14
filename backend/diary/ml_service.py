from typing import Dict, List, Tuple  # <-- Añade los 'types' de vuelta

from decouple import config
from gradio_client import Client

# --- 1. CONFIGURACIÓN A NIVEL DE MÓDULO ---

# Lee la URL de tu variable de entorno en Railway
HF_SPACE_URL = config("HF_SPACE_URL")

# --- 2. CREA EL CLIENTE UNA SOLA VEZ ---
# Esto se ejecuta solo cuando Railway inicia tu app (gunicorn)
print(f"🔄 Conectando al cliente de Gradio en: {HF_SPACE_URL}")
try:
    # Creamos el cliente de forma global para reutilizarlo
    API_CLIENT = Client(HF_SPACE_URL)
    print("✅ Cliente de Gradio conectado y listo.")
except Exception as e:
    print(f"❌ ERROR CRÍTICO: No se pudo conectar al Gradio Space: {e}")
    API_CLIENT = None

# --- 3. FUNCIÓN DE PREDICCIÓN (AHORA MÁS RÁPIDA) ---


def analizar_emociones_con_beto(texto: str) -> Tuple[List[str], Dict[str, float]]:
    """
    Analiza las emociones de un texto llamando a la API
    desplegada en Hugging Face Spaces.
    """

    # Si el cliente no se pudo crear al inicio, falla rápido
    if API_CLIENT is None:
        print("Error: API_CLIENT no está inicializado.")
        return ["error_api"], {}

    try:
        # Usa el cliente global (mucho más rápido)
        result = API_CLIENT.predict(texto, api_name="/predict")

        # El 'result' es el diccionario JSON que definiste en tu Space
        # ej: {"emociones": ["alegria"], "probabilidades": {...}}
        emociones = result.get("emociones", ["error_parseo"])
        probabilidades = result.get("probabilidades", {})

        return emociones, probabilidades

    except Exception as e:
        print(f"❌ Error durante la predicción en Gradio Space: {e}")
        return ["error_api"], {}
