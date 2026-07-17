from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import secrets
import random
import time

app = FastAPI()

SESSIONS = {}


class Generate(BaseModel):
    web: str


class Validate(BaseModel):
    session: str
    client_id: str
    web: str


@app.get("/")
def home():
    return {"status": "online"}


# =========================
# GENERATE
# =========================
@app.post("/generate")
def generate(data: Generate):

    # Hapus session expired
    now = time.time()
    for sid in list(SESSIONS.keys()):
        if now > SESSIONS[sid]["expired"]:
            del SESSIONS[sid]

    key = "".join(str(random.randint(0, 9)) for _ in range(10))
    session = secrets.token_hex(16)

    SESSIONS[session] = {
        "key": key,
        "web": data.web,
        "client_id": None,
        "verified": False,
        "expired": now + 10800
    }

    return {
        "success": True,
        "key": key,
        "session": session
    }


# =========================
# VERIFY
# =========================
@app.get("/verify", response_class=HTMLResponse)
def verify(kode: str):

    target = None

    for sid, item in SESSIONS.items():
        if item["key"] == kode:
            target = sid
            break

    if target is None:
        return "<h2>❌ KEY TIDAK DITEMUKAN</h2>"

    item = SESSIONS[target]

    if time.time() > item["expired"]:
        del SESSIONS[target]
        return "<h2>⌛ KEY EXPIRED</h2>"

    item["verified"] = True

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Verify</title>
    </head>
    <body style="font-family:Arial;text-align:center;margin-top:80px">
        <h2>✅ KEY BERHASIL DIVERIFIKASI</h2>
        <h3>{kode}</h3>
        <p>Silakan kembali ke bot.</p>
    </body>
    </html>
    """


# =========================
# VALIDATE
# =========================
@app.post("/validate")
def validate(data: Validate):

    if data.session not in SESSIONS:
        return {
            "success": False,
            "message": "session tidak ditemukan"
        }

    item = SESSIONS[data.session]

    if time.time() > item["expired"]:
        del SESSIONS[data.session]
        return {
            "success": False,
            "message": "expired"
        }

    if not item["verified"]:
        return {
            "success": False,
            "message": "belum verify"
        }

    if item["web"] != data.web:
        return {
            "success": False,
            "message": "web tidak cocok"
        }

    # Pertama kali login
    if item["client_id"] is None:
        item["client_id"] = data.client_id

    # Client berbeda
    elif item["client_id"] != data.client_id:
        return {
            "success": False,
            "message": "client tidak sesuai"
        }

    return {
        "success": True,
        "message": "KEY VALID",
        "expired": int(item["expired"] - time.time())
        }
