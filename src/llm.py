import json
from .config import get_api_key

SYSTEM = "You are a practical career coach. Be specific, honest, concise, and never invent experience, qualifications, or metrics for the candidate."


def _openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=get_api_key("OpenAI"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _groq(prompt: str) -> str:
    from groq import Groq
    client = Groq(api_key=get_api_key("Groq"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _gemini(prompt: str) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=get_api_key("Gemini"))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2),
    )
    return response.text


def ask_llm(provider: str, prompt: str) -> dict | None:
    if not get_api_key(provider):
        return None
    raw = {"OpenAI": _openai, "Groq": _groq, "Gemini": _gemini}[provider](prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
