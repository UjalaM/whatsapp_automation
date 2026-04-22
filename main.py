from fastapi import FastAPI, Request
from bot_logic import get_reply
from whatsapp import send_whatsapp_message

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/webhook")
async def webhook(request: Request):
    form = await request.form()

    user_msg = form.get("Body")
    user_number = form.get("From").replace("whatsapp:", "")

    print(f"Message from {user_number}: {user_msg}")

    reply = get_reply(user_number, user_msg)

    send_whatsapp_message(user_number, reply)

    return {"status": "ok"}