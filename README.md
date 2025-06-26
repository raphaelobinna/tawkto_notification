
# 🕵️‍♂️ Tawk.to Webhook Listener (FastAPI)

A simple FastAPI-based webhook receiver for Tawk.to that:

- Verifies webhook authenticity using **HMAC-SHA1** with the `X-Tawk-Signature` header  
- Logs incoming headers, raw body, and verification details  
- Parses JSON payloads and logs chat events

---

## 📦 Features

- **Signature verification**: protects against spoofed requests  
- **Structured logging**: outputs signature, digests, and payload  
- **FastAPI endpoint**: `/tawk-webhook` to receive POST requests  
- **Flexible logging setup** using Python’s `logging` module

---

## 📋 Prerequisites

- Python 3.10+  
- Dependencies in `requirements.txt`:

```

fastapi
uvicorn
pydantic-settings
python-dotenv

````

---

## ⚙️ Setup

1. **Clone or download this repo**  
2. **Copy `.env.example` to `.env`** with your secret:

```env
TAWK_TAWK_WEBHOOK_SECRET=your_secret_here
````

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

---

## 🔐 Signature Verification

Tawk.to webhooks include an `X-Tawk-Signature` header, which is an **HMAC-SHA1** hash of the raw, unparsed request body. The app:

1. Reads the `tawk_webhook_secret` from `.env`
2. Computes SHA1 HMAC of the incoming raw body
3. Compares it to `X-Tawk-Signature` using a secure `compare_digest()`
4. Logs mismatch and continues — adjust to reject if needed

---

## 📩 Webhook Endpoint

* **URL**: `/tawk-webhook`
* **Method**: `POST`
* **Behavior**:

  * Logs received signature, computed digest, raw JSON, and parsed data
  * Returns `200 OK` with `{"status":"ok"}`
  * Change `raise HTTPException(status=403)` to actually reject invalid requests

---

## 🛠️ Logging Configuration

* Logs go to `stdout` via `StreamHandler`, suitable for containerized environments (e.g., Cloud Run)
* Logged info includes:

  * Raw headers & body
  * Signature vs digest comparison
  * Entire parsed JSON payload

---

## 🚀 Deployment

Works in any ASGI-compatible environment:

* **Locally**: `uvicorn main:app`
* **Docker**: map port & ensure `ENV PYTHONUNBUFFERED=1` in Dockerfile
* **Cloud Run** / **Heroku** / **FastAPI-compatible platforms**

---

## 🧩 Next Steps

* Add push notifications when agents reply
* Store incoming data in a database
* Handle multiple event types (`chat:start`, `chat:end`, etc.)
* Implement proper response behavior (return 403 to reject)

---

## 🔏 Security Notes

* Do **not log** webhook secrets or authentication info
* Optionally enforce HTTPS and IP allowlist
* If a mismatch is critical, re-enable the `403 Forbidden` exception

---

## 🛰️ License

MIT © 2025 Your Name or Organization

```

---

Feel free to adjust host, port, rejection behavior, or next-step suggestions as needed!
```
