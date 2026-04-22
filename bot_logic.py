import os
from openai import OpenAI

_api_key = os.getenv("OPENROUTER_API_KEY")
if not _api_key:
    print("[STARTUP ERROR] OPENROUTER_API_KEY is not set or empty!")
else:
    print(f"[STARTUP] OPENROUTER_API_KEY loaded (starts with: {_api_key[:10]}...)")

client = OpenAI(
    api_key=_api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://whatsapp-automation-jsy3.onrender.com",
        "X-Title": "WhatsApp Bot",
    },
)

# Load knowledge base once at startup
_KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
with open(_KB_PATH, "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE = f.read()

SYSTEM_PROMPT = f"""You are a helpful WhatsApp assistant for a multi-domain business.
You have access to the following knowledge base that covers three business domains:
1. Real Estate (Sunshine Realty)
2. Coaching Centre (BrightMind Academy)
3. Clinic (HealthFirst Multi-Speciality Clinic)

Use ONLY the information in the knowledge base below to answer user queries.
If the user's question is outside these domains or the information is not in the knowledge base,
politely say you don't have that information and suggest they contact the relevant team directly.

Keep your replies concise, friendly, and formatted for WhatsApp (avoid heavy markdown; use plain text with emojis where appropriate).
Always end your reply with an offer to help further.

KNOWLEDGE BASE:
{KNOWLEDGE_BASE}
"""

# Stores per-user conversation history: {{ phone: [{{role, content}}, ...] }}
conversation_history: dict[str, list[dict]] = {}

MAX_HISTORY_TURNS = 10  # keep last 10 exchanges to limit token usage


def get_reply(phone: str, message: str) -> str:
    if phone not in conversation_history:
        conversation_history[phone] = []

    history = conversation_history[phone]
    history.append({"role": "user", "content": message})

    # Trim old turns to stay within context limit
    if len(history) > MAX_HISTORY_TURNS * 2:
        history = history[-(MAX_HISTORY_TURNS * 2):]
        conversation_history[phone] = history

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            temperature=0.4,
            max_tokens=500,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Sorry, I'm having trouble responding right now. Please try again in a moment. 🙏"
        print(f"[LLM ERROR] {e}")

    history.append({"role": "assistant", "content": reply})
    return reply


def reset_conversation(phone: str) -> None:
    """Clear the conversation history for a user (e.g., on 'reset' or 'start over')."""
    conversation_history.pop(phone, None)
