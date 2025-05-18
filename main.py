from fastapi import FastAPI, Form, Request
from twilio.twiml.voice_response import VoiceResponse, Dial, Number, Client
from fastapi.responses import Response
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import twilio
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("twilio_app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Allow Flutter dev server to call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/token")
def get_twilio_token(identity: str = Query(...)):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    api_key = os.getenv("TWILIO_API_KEY")
    api_secret = os.getenv("TWILIO_API_SECRET")
    app_sid = os.getenv("TWILIO_VOICE_APP_SID")

    if not all([account_sid, api_key, api_secret, app_sid]):
        return {"error": "Twilio credentials are missing"}

    # Create access token
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create voice grant
    voice_grant = VoiceGrant(
        outgoing_application_sid=app_sid,
        incoming_allow=True  # optional: allows incoming calls
    )
    token.add_grant(voice_grant)
    print(token.to_jwt())
    return {"token": token.to_jwt()}


@app.post("/voice")
async def voice_handler(
    To: str = Query(...),
    From: str = Query(...),
):
    logger.info(f"[VOICE] Incoming call: From={From}, To={To}")

    response = VoiceResponse()
    dial = Dial(caller_id=From)

    try:
        if To.startswith('+'):  # outbound phone number
            logger.info(f"[DIAL] Dialing external number: {To}")
            dial.append(Number(To))  # ✅ Append a Number object
        else:
            logger.info(f"[DIAL] Dialing Twilio Client ID: {To}")
            dial.append(Client(To))  # ✅ Append a Client object

        response.append(dial)

        # ✅ Return the TwiML XML string explicitly
        logger.info(f"[RESPONSE] {response}")
        return Response(content=str(response), media_type="application/xml")

    except Exception as e:
        logger.error(f"[ERROR] Failed to process call: {e}")
        fallback = VoiceResponse()
        fallback.say(
            "We’re sorry, an error occurred while connecting your call.")
        return Response(content=str(fallback), media_type="application/xml")
