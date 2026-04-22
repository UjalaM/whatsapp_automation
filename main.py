from fastapi import FastAPI, Request
from bot_logic import get_reply, reset_conversation
from whatsapp import send_whatsapp_message

app = FastAPI()

RESET_KEYWORDS = {"reset", "start over", "restart", "clear", "new chat"}

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/webhook")
async def webhook(request: Request):
    form = await request.form()

    user_msg = form.get("Body", "").strip()
    user_number = form.get("From", "").replace("whatsapp:", "")

    print(f"Message from {user_number}: {user_msg}")

    if user_msg.lower() in RESET_KEYWORDS:
        reset_conversation(user_number)
        reply = "Conversation reset! 👋 How can I help you today? I can assist with Real Estate, Coaching Courses, or Clinic appointments."
    else:
        reply = get_reply(user_number, user_msg)

    send_whatsapp_message(user_number, reply)

    return {"status": "ok"}