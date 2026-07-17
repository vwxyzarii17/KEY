from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
import random
import time

app = FastAPI()

KEYS = {}


class Validate(BaseModel):
    key: str
    client_id: str


@app.get("/")
def home():
    return {"status": "online"}


@app.get("/generate", response_class=PlainTextResponse)
def generate():

    key = "".join(str(random.randint(0, 9)) for _ in range(10))

    KEYS[key] = {
        "expired": time.time() + 10800,  # 3 jam
        "verified": False,
        "client_id": None
    }

    return f"KEY: {key}"


@app.get("/verify", response_class=HTMLResponse)
def verify(kode: str):

    if kode not in KEYS:
        return "<h2>❌ KEY TIDAK DITEMUKAN</h2>"

    if time.time() > KEYS[kode]["expired"]:
        del KEYS[kode]
        return "<h2>⌛ KEY SUDAH EXPIRED</h2>"

    KEYS[kode]["verified"] = True

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Verify Key</title>
        <meta charset="UTF-8">
    </head>
    <body style="font-family:Arial;text-align:center;margin-top:60px">
        <h2>✅ KEY BERHASIL DIVERIFIKASI</h2>
        <h3>{kode}</h3>
    </body>
    </html>
    """


@app.post("/validate")
def validate(data: Validate):

    if data.key not in KEYS:
        return {
            "success": False,
            "message": "key tidak ditemukan"
        }

    key_data = KEYS[data.key]

    if time.time() > key_data["expired"]:
        del KEYS[data.key]
        return {
            "success": False,
            "message": "expired"
        }

    if not key_data["verified"]:
        return {
            "success": False,
            "message": "belum verify"
        }

    # Ikat ke client pertama
    if key_data["client_id"] is None:
        key_data["client_id"] = data.client_id

    # Tolak jika client berbeda
    elif key_data["client_id"] != data.client_id:
        return {
            "success": False,
            "message": "key digunakan oleh client lain"
        }

    return {
        "success": True,
        "message": "KEY VALID"
    }
