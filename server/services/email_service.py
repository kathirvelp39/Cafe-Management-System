import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email(to_email: str, subject: str, body: str, attachment_path: str = None):
    """
    Sends an email using the configured SMTP credentials.
    """
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("Warning: SMTP credentials not configured. Email not sent.")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg.set_content(body)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        
        msg.add_attachment(
            file_data,
            maintype='application',
            subtype='pdf',
            filename=file_name
        )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        raise e
