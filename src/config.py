from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROVIDERS = {
    "OpenAI": "OPENAI_API_KEY",
    "Groq": "GROQ_API_KEY",
    "Gemini": "GOOGLE_API_KEY",
}


def get_api_key(provider: str) -> str | None:
    """Read provider credentials from Streamlit Secrets or local environment."""
    key_name = PROVIDERS.get(provider)
    if not key_name:
        return None

    # Streamlit Community Cloud stores deployment secrets in st.secrets.
    # Local development can continue using .env / environment variables.
    try:
        import streamlit as st

        secret_value = st.secrets.get(key_name)
        if secret_value:
            return str(secret_value)
    except Exception:
        pass

    return os.getenv(key_name)


def ensure_upload_dir() -> Path:
    path = Path("data/uploads")
    path.mkdir(parents=True, exist_ok=True)
    return path
