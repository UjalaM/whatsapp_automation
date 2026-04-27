import os
from openai import OpenAI

_api_key = os.getenv("OPENROUTER_API_KEY")
if not _api_key:
    print("[STARTUP ERROR] OPENROUTER_API_KEY is not set or empty!")
else:
    print(f"[STARTUP] OPENROUTER_API_KEY loaded (starts with: {_api_key[:10]}...)")

# Set BOT_SECTOR in env: "salon" | "ac" | "dental"
# This determines which business this bot instance serves.
BOT_SECTOR = os.getenv("BOT_SECTOR", "salon")

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

# ─────────────────────────────────────────────
# STATIC MENU MESSAGES  (zero LLM cost)
# ─────────────────────────────────────────────

GREETING_MSG = "Hi! 👋 Thanks for reaching out. How can I help you today?"

SECTOR_MENU = {
    "salon": (
        "💇 *Salon Services*\n\n"
        "What would you like to know?\n\n"
        "1️⃣  Services & Pricing\n"
        "2️⃣  Timings & Location\n"
        "3️⃣  Book an Appointment\n"
        "4️⃣  Ask a Question\n\n"
        "Reply with a number or just type your question 😊"
    ),
    "ac": (
        "❄️ *AC Repair & Home Services*\n\n"
        "What would you like to know?\n\n"
        "1️⃣  Services & Pricing\n"
        "2️⃣  Areas Covered & Timings\n"
        "3️⃣  Book a Service Visit\n"
        "4️⃣  Ask a Question\n\n"
        "Reply with a number or just type your question 😊"
    ),
    "dental": (
        "🦷 *Dental Clinic*\n\n"
        "What would you like to know?\n\n"
        "1️⃣  Treatments & Pricing\n"
        "2️⃣  Timings & Location\n"
        "3️⃣  Book an Appointment\n"
        "4️⃣  Ask a Question\n\n"
        "Reply with a number or just type your question 😊"
    ),
}

SECTOR_INFO = {
    "salon": {
        "pricing": (
            "💇 *Salon Services & Pricing*\n\n"
            "*Hair (Women):*\n"
            "• Haircut & Styling: ₹300–₹700\n"
            "• Straightening: ₹2,500–₹6,000\n"
            "• Keratin Treatment: ₹3,000–₹8,000\n"
            "• Hair Color: ₹1,500–₹4,000\n"
            "• Hair Spa: ₹800–₹2,000\n\n"
            "*Hair (Men):*\n"
            "• Haircut: ₹150–₹400\n"
            "• Beard Trim: ₹100–₹250\n"
            "• Hair Spa: ₹600–₹1,200\n\n"
            "*Skin & Face:*\n"
            "• Basic Facial: ₹500–₹1,000\n"
            "• Gold/Diamond Facial: ₹1,500–₹3,000\n"
            "• Waxing (Full Body): ₹1,500–₹2,500\n\n"
            "*Bridal:*\n"
            "• Bridal Makeup: ₹5,000–₹15,000\n"
            "• Pre-Bridal Package: ₹8,000–₹20,000\n\n"
            "Reply *3* to book an appointment or *4* to ask anything 😊"
        ),
        "timing": (
            "🕐 *Timings & Location*\n\n"
            "📅 Mon–Sat: 10:00 AM – 9:00 PM\n"
            "📅 Sunday: 11:00 AM – 7:00 PM\n\n"
            "📍 Andheri West, Mumbai\n"
            "(Near Lokhandwala Market)\n\n"
            "Walk-ins welcome. Appointments get priority! ✅\n\n"
            "Reply *3* to book an appointment"
        ),
    },
    "ac": {
        "pricing": (
            "❄️ *AC Repair Services & Pricing*\n\n"
            "• AC Service / Cleaning: ₹400–₹700\n"
            "• Deep Cleaning (Jet Wash): ₹800–₹1,500\n"
            "• Gas Refilling (1.5 Ton): ₹1,500–₹2,500\n"
            "• AC Installation (Split): ₹1,500–₹2,500\n"
            "• Compressor Repair: ₹3,000–₹8,000\n"
            "• AMC (Annual Contract): ₹1,200–₹2,500/year\n\n"
            "*Brands:* Voltas, Daikin, LG, Samsung, Blue Star, Hitachi & more\n\n"
            "🔧 30-day warranty on all repairs\n"
            "✅ Free diagnosis — charged only if you proceed\n\n"
            "Reply *3* to book a service visit"
        ),
        "timing": (
            "🕐 *Areas Covered & Timings*\n\n"
            "📅 Mon–Sat: 8:00 AM – 8:00 PM\n"
            "📅 Sunday: 9:00 AM – 5:00 PM\n"
            "🚨 Emergency calls: 7 days a week\n\n"
            "📍 *Areas Covered:*\n"
            "Andheri, Goregaon, Malad, Kandivali, Borivali,\n"
            "Thane, Navi Mumbai, Powai, Bandra, Santacruz, Vile Parle\n\n"
            "⚡ Same-day service for urgent calls!\n\n"
            "Reply *3* to book a service visit"
        ),
    },
    "dental": {
        "pricing": (
            "🦷 *Dental Treatments & Pricing*\n\n"
            "*General:*\n"
            "• Checkup & Consultation: ₹300\n"
            "• Teeth Cleaning (Scaling): ₹600–₹1,200\n"
            "• Tooth Filling: ₹800–₹2,000\n"
            "• Root Canal (RCT): ₹3,500–₹6,000\n"
            "• Tooth Extraction: ₹500–₹1,500\n\n"
            "*Cosmetic:*\n"
            "• Teeth Whitening: ₹5,000–₹12,000\n"
            "• Veneers (per tooth): ₹8,000–₹15,000\n\n"
            "*Braces & Aligners:*\n"
            "• Metal Braces: ₹20,000–₹35,000\n"
            "• Clear Aligners: ₹50,000–₹1,20,000\n\n"
            "*Implants:*\n"
            "• Single Implant: ₹25,000–₹45,000\n\n"
            "💳 EMI available | Insurance accepted\n\n"
            "Reply *3* to book an appointment"
        ),
        "timing": (
            "🕐 *Timings & Location*\n\n"
            "📅 Mon–Sat: 10:00 AM – 8:00 PM\n"
            "📅 Sunday: 10:00 AM – 2:00 PM\n\n"
            "📍 Andheri West, Mumbai\n\n"
            "🚨 Emergency dental care available — same-day slots for severe pain\n\n"
            "Reply *3* to book an appointment"
        ),
    },
}

SECTOR_LABEL = {
    "salon": "salon appointment",
    "ac": "AC service visit",
    "dental": "dental appointment",
}

LLM_SYSTEM = {
    "salon": "You are a WhatsApp assistant for a salon. Answer only salon-related questions using the knowledge base.",
    "ac": "You are a WhatsApp assistant for an AC repair service. Answer only AC/home appliance repair questions using the knowledge base.",
    "dental": "You are a WhatsApp assistant for a dental clinic. Answer only dental/clinic questions using the knowledge base. Never give specific medical advice.",
}

# ─────────────────────────────────────────────
# STATE STORE
# ─────────────────────────────────────────────

# state shape: { "step": str, "sector": str|None, "data": dict, "history": list }
user_states: dict[str, dict] = {}

GREETING_TRIGGERS = {"hi", "hello", "hey", "start", "menu", "hii", "helo", "helo", "namaste"}
RESET_TRIGGERS = {"reset", "start over", "restart", "clear", "main menu", "back"}


def _fresh_state() -> dict:
    return {"step": "sector_menu", "sector": BOT_SECTOR, "data": {}, "history": []}


# ─────────────────────────────────────────────
# MAIN HANDLER
# ─────────────────────────────────────────────

def get_reply(phone: str, message: str) -> str:
    msg = message.strip()
    msg_lower = msg.lower()

    # Always reset on greeting or reset keyword
    if msg_lower in GREETING_TRIGGERS or msg_lower in RESET_TRIGGERS:
        user_states[phone] = _fresh_state()
        return GREETING_MSG + "\n\n" + SECTOR_MENU[BOT_SECTOR]

    state = user_states.get(phone, _fresh_state())
    user_states[phone] = state
    step = state["step"]

    # ── SECTOR MENU: waiting for sub-option ──
    if step == "sector_menu":
        sector = state["sector"]

        if msg == "1":
            return SECTOR_INFO[sector]["pricing"]

        elif msg == "2":
            return SECTOR_INFO[sector]["timing"]

        elif msg == "3":
            state["step"] = "lead_name"
            label = SECTOR_LABEL[sector]
            return f"Great! Let's get your {label} scheduled. 📋\n\nFirst, may I know your *name*?"

        elif msg == "4":
            state["step"] = "llm"
            return "Sure! Go ahead and type your question 👇"

        else:
            # Free-text → route to LLM with sector context
            state["step"] = "llm"
            return _llm_reply(state, msg)

    # ── LEAD CAPTURE: name ──
    if step == "lead_name":
        state["data"]["name"] = msg
        state["step"] = "lead_req"
        sector = state["sector"]
        if sector == "ac":
            return f"Thanks {msg}! 😊\n\nWhat is the issue with your AC? (e.g. not cooling, gas refill, installation, noise)"
        elif sector == "salon":
            return f"Thanks {msg}! 😊\n\nWhat service are you looking for? (e.g. haircut, keratin, facial, bridal)"
        else:
            return f"Thanks {msg}! 😊\n\nWhat is the concern or treatment you are looking for?"

    # ── LEAD CAPTURE: requirement ──
    if step == "lead_req":
        state["data"]["requirement"] = msg
        state["step"] = "lead_time"
        return "What is your *preferred date and time*? ⏰\n(e.g. Tomorrow 4 PM, Saturday morning)"

    # ── LEAD CAPTURE: time → done ──
    if step == "lead_time":
        state["data"]["preferred_time"] = msg
        name = state["data"].get("name", "")
        req = state["data"].get("requirement", "")
        time = state["data"].get("preferred_time", "")
        label = SECTOR_LABEL.get(state["sector"], "appointment")

        summary = (
            f"✅ *Booking Request Received!*\n\n"
            f"👤 Name: {name}\n"
            f"📋 Requirement: {req}\n"
            f"🕐 Preferred Time: {time}\n\n"
            f"Our team will contact you shortly to confirm your {label}. 😊\n\n"
            f"Is there anything else I can help you with? Reply *menu* to go back to the main menu."
        )
        state["step"] = "sector_menu"
        state["data"] = {}
        return summary

    # ── LLM MODE: free-text questions ──
    if step == "llm":
        return _llm_reply(state, msg)

    # Fallback
    user_states[phone] = _fresh_state()
    return SECTOR_MENU[BOT_SECTOR]


# ─────────────────────────────────────────────
# LLM HELPER  (called only for free-text)
# ─────────────────────────────────────────────

MAX_HISTORY = 8

def _llm_reply(state: dict, message: str) -> str:
    sector = state.get("sector")
    history = state.setdefault("history", [])

    system_context = LLM_SYSTEM.get(sector, "You are a helpful WhatsApp assistant for a small business.")
    full_system = f"{system_context}\n\nKNOWLEDGE BASE:\n{KNOWLEDGE_BASE}\n\nKeep replies short and WhatsApp-friendly. Use plain text with light emojis. Always offer a helpful next step."

    history.append({"role": "user", "content": message})
    if len(history) > MAX_HISTORY * 2:
        history = history[-(MAX_HISTORY * 2):]
        state["history"] = history

    messages = [{"role": "system", "content": full_system}] + history

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            messages=messages,
            temperature=0.4,
            max_tokens=400,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Sorry, I'm having trouble right now. Please try again in a moment. 🙏"
        print(f"[LLM ERROR] {e}")

    history.append({"role": "assistant", "content": reply})
    return reply


def reset_conversation(phone: str) -> None:
    user_states.pop(phone, None)
