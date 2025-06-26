from fastapi import FastAPI, Request, HTTPException, status
import hmac, hashlib
from config import settings

app = FastAPI()


# print(settings.tawk_webhook_secret)

def verify_signature(raw_body: bytes, signature: str) -> bool:
    digest = hmac.new(settings.tawk_webhook_secret.encode(), raw_body, hashlib.sha1).hexdigest()
    return hmac.compare_digest(digest, signature)

@app.post("/tawk-webhook")
async def tawk_webhook(request: Request):
    raw_body = await request.body()
    signature = request.headers.get("X-Tawk-Signature", "")
    if not verify_signature(raw_body, signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")

    data = await request.json()
    print("📩 Received Tawk.to webhook payload:")
    print(data)

    return {"status": "ok"}
