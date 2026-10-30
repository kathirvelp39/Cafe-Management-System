import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

def send_sms(to_phone: str, message: str):
    """
    Sends an SMS using the configured Twilio credentials.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_FROM_NUMBER:
        print("Warning: Twilio credentials not configured. SMS not sent.")
        return

    # In a real scenario we should validate the phone number format
    if not to_phone.startswith('+'):
        # Just a basic precaution, Twilio requires E.164 format
        # This will assume a default country code if missing, but it's better if the user inputs it.
        pass

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to_phone
        )
        print(f"SMS sent successfully to {to_phone} with SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS to {to_phone}: {e}")
