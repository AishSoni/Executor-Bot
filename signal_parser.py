import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

def extract_signal(text):
    prompt = f"""
You are a trading signal parser. Extract structured fields from the following text:

{text}

Return in JSON:
symbol: (e.g., SUIUSDT)
position: (long/short)
leverage: (e.g., 3x-5x)
entries: list of floats
targets: list of floats
stop_loss: value or condition
notes: list of strings (if any)
"""

    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )
    return eval(response.json()['response'])  # safer to use `json.loads` if output is strict JSON
