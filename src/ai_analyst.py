"""
AI Threat Intelligence Analyst.
Uses an LLM to analyze phishing messages with a fallback architecture.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", "dummy_key")
)

# Lista de modelos gratuitos de respaldo
FALLBACK_MODELS = [
    "google/gemma-4-26b-a4b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-r1:free",
    "microsoft/phi-3-mini-128k-instruct:free"
]

def generate_threat_report(message: str, findings: list) -> str:
    """Genera un reporte de inteligencia de amenazas usando el LLM con Fallback."""
    
    if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "dummy_key":
        return "⚠️ AI Analyst disabled. Missing OPENROUTER_API_KEY in .env."

    findings_text = "\n".join([f"- {f}" for f in findings])

    system_prompt = """
    You are a Senior Cyber Threat Intelligence Analyst specializing in North Korean APT groups (like Lazarus/TraderTraitor).
    A user has submitted a suspicious message. Our static scanner (Regex) found these red flags:
    
    {findings}
    
    Your job is to write a concise Threat Intelligence Report:
    1. Explain the psychology of the attack (e.g., social engineering, urgency).
    2. Identify what the attacker is trying to achieve (e.g., malware execution, credential theft).
    3. Give a 1-sentence recommendation on what the user should do.
    
    Keep the tone professional, urgent, and analytical. Use Markdown.
    """.format(findings=findings_text)

    # Bucle de Fallback: Intenta con cada modelo hasta que uno funcione
    for model_name in FALLBACK_MODELS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Here is the suspicious message:\n\n{message}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Model {model_name} failed: {error_msg}. Trying next...")
            # Si el error es 404 (no existe) o 429 (saturado), pasamos al siguiente modelo
            continue

    # Si todos los modelos fallan
    return "❌ AI Analysis failed. All fallback models are currently unavailable or rate-limited. Please try again in a few minutes."