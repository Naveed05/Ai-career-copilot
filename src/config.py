from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROVIDERS = {
    "OpenAI": "OPENAI_API_KEY",
    "Groq": "GROQ_API_KEY",
    "Gemini": "GOOGLE_API_KEY",
}


def get_api_key(provider: str) -> str | None:
    key_name = PROVIDERS.get(provider)
    return os.getenv(key_name) if key_name else None


def ensure_upload_dir() -> Path:
    path = Path("data/uploads")
    path.mkdir(parents=True, exist_ok=True)
    return path
