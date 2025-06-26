from fastapi import FastAPI, Request, HTTPException, status
import hmac, hashlib
from config import settings
import hmac, hashlib, logging, sys

app = FastAPI()

# Setup logger
logger = logging.getLogger("tawk")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False


print(settings.tawk_webhook_secret)

def verify_signature(raw_body: bytes, signature: str) -> bool:
    digest = hmac.new(settings.tawk_webhook_secret.encode(), raw_body, hashlib.sha1).hexdigest()
    return hmac.compare_digest(digest, signature)

@app.post("/tawk-webhook")
async def tawk_webhook(request: Request):
    raw = await request.body()
    signature = request.headers.get("X-Tawk-Signature", "")
    digest = hmac.new(settings.tawk_webhook_secret.encode(), raw, hashlib.sha1).hexdigest()

    logger.info("Incoming X-Tawk-Signature: %s", signature)
    logger.info("Expected digest         : %s", digest)
    logger.info("Raw body (json): %s", raw.decode('utf-8'))

    if not hmac.compare_digest(signature, digest):
        logger.warning("❌ Signature mismatch")
        raise HTTPException(403, "Invalid signature")

    data = await request.json()
    logger.info("✅ Valid webhook, payload: %s", data)
    return {"status": "ok"}
