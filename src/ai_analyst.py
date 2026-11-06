"""
AI Threat Intelligence Analyst using Groq API.
Uses the OpenAI SDK but points to Groq's high-speed infrastructure.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuración del cliente apuntando a Groq
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY", "dummy_key")
)

# Modelo gratuito y ultra-rápido de Groq
MODEL = "openai/gpt-oss-20b"

def generate_threat_report(message: str, findings: list) -> str:
    """Genera un reporte de inteligencia de amenazas usando Groq."""
    
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "dummy_key":
        return "⚠️ AI Analyst disabled. Missing GROQ_API_KEY in .env."

    findings_text = "\n".join([f"- {f}" for f in findings])

    system_prompt = f"""
    You are a Senior Cyber Threat Intelligence Analyst specializing in North Korean APT groups (like Lazarus/TraderTraitor).
    A user has submitted a suspicious message. Our static scanner (Regex) found these red flags:
    
    {findings_text}
    
    Your job is to write a concise Threat Intelligence Report:
    1. Explain the psychology of the attack (e.g., social engineering, urgency).
    2. Identify what the attacker is trying to achieve (e.g., malware execution, credential theft).
    3. Give a 1-sentence recommendation on what the user should do.
    
    Keep the tone professional, urgent, and analytical. Use Markdown.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the suspicious message:\n\n{message}"}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ AI Analysis failed: {str(e)}"