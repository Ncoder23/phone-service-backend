# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
import dotenv

dotenv.load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
FROM_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]
client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml="<Response><Say>Ahoy, World!</Say></Response>",
    to="+14082072011",
    from_=FROM_NUMBER,
)

print(call.sid)
