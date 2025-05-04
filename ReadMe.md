# 📞 Phone Translator Backend (FastAPI + Twilio)

This FastAPI backend powers a voice translation app using Twilio Programmable Voice. It includes:

- 🔐 Token generation for Twilio Client registration
- 🛠️ TwiML handler to route outgoing calls (to phone or client)
- 🧾 Logging support for tracing call flows
- 🚀 Deployable to Render or Fly.io

---

## 🧠 Features

- Issue secure access tokens for Twilio Voice SDK
- Dynamically dial phone numbers or Twilio client identities
- Return TwiML instructions via `/voice`
- Supports HTTPS deployments with env config

---

## ⚙️ Requirements

- Python 3.8+
- Twilio Account (SID, API Key, Voice App SID)
