from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Twilio
TWILIO_PHONE_NUM = os.getenv('TWILIO_PHONE_NUM')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TO_PHONE_NUM = os.getenv('MY_PHONE_NUM')

class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    def send_sms(self,message):
        
        resp = self.client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUM,
            to=TO_PHONE_NUM
        )

        print(resp.sid)