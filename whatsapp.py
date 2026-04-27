from twilio.rest import Client
import os

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")

client = Client(account_sid, auth_token)

TWILIO_FROM = "whatsapp:+14155238886"


def send_whatsapp_message(to: str, message: str) -> None:
    client.messages.create(
        body=message,
        from_=TWILIO_FROM,
        to=f"whatsapp:{to}",
    )
