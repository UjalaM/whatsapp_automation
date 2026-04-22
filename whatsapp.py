from twilio.rest import Client
import os

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")

client = Client(account_sid, auth_token)

def send_whatsapp_message(to, message):
    client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Twilio sandbox number
        to=f'whatsapp:{to}'
    )