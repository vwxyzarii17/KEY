from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
import random
import time

app = FastAPI()

KEYS = {}

class Validate(BaseModel):
    key: str


@app.get("/")
def home():
    return {"status": "online"}


# FILE VERIFIKASI CLİKER ADS
@app.get(
    "/verify_a0bd63d949f31dff8cf54ba9895456e87f799577.txt",
    response_class=PlainTextResponse
)
def clikerads_verify():
    return "ISI_KODE_VERIFIKASI_DARI_CLIKER_ADS"


@app.get("/generate", response_class=PlainTextResponse)
def generate():
    key = "".join(
        str(random.randint(0, 9))
        for _ in range(10)
    )

    KEYS[key] = {
        "expired": time.time() + 3600,
        "verified": False
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
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify Key</title>
    </head>

    <body style="
        font-family:Arial;
        text-align:center;
        padding:50px 15px;
    ">

        <h1>✅ KEY BERHASIL<br>DIVERIFIKASI</h1>

        <h2>{kode}</h2>

        <div style="
            width:100%;
            max-width:728px;
            min-height:100px;
            margin:30px auto;
        ">
            <div
                id="clikerads-banner"
                data-code="2BF04D80">
            </div>
        </div>

        <script src="https://clikerads.com/banner.js"></script>

        <p>Key berlaku selama 1 jam.</p>

    </body>
    </html>
    """


@app.post("/validate")
def validate(data: Validate):

    key = data.key

    if key not in KEYS:
        return {
            "success": False,
            "message": "key tidak ditemukan"
        }

    if time.time() > KEYS[key]["expired"]:
        del KEYS[key]

        return {
            "success": False,
            "message": "expired"
        }

    if not KEYS[key]["verified"]:
        return {
            "success": False,
            "message": "belum verify"
        }

    return {
        "success": True,
        "message": "KEY VALID"
    }