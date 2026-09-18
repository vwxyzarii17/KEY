from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
import random
import time
import re

app = FastAPI()

KEYS = {}


# ==========================================
# CLIKER ADS VERIFICATION
# ==========================================

@app.get(
    "/verify_{token}.txt",
    response_class=PlainTextResponse
)
def clikerads_verification(token: str):

    # Pastikan token hanya karakter hex
    if not re.fullmatch(r"[a-fA-F0-9]+", token):
        return PlainTextResponse(
            "Invalid verification token",
            status_code=404
        )

    # Kembalikan token PERSIS
    return token


class Validate(BaseModel):
    key: str


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "status": "online"
    }


# ==========================================
# GENERATE KEY
# ==========================================

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


# ==========================================
# VERIFY KEY
# ==========================================

@app.get("/verify", response_class=HTMLResponse)
def verify(kode: str):

    if kode not in KEYS:
        return """
        <h2>❌ KEY TIDAK DITEMUKAN</h2>
        """

    if time.time() > KEYS[kode]["expired"]:

        del KEYS[kode]

        return """
        <h2>⌛ KEY SUDAH EXPIRED</h2>
        """

    KEYS[kode]["verified"] = True

    return f"""
    <!DOCTYPE html>
    <html lang="id">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Verify Key</title>

        <style>
            body {{
                margin: 0;
                padding: 50px 15px;
                font-family: Arial;
                text-align: center;
                background: #ffffff;
            }}

            .success {{
                font-size: 30px;
                font-weight: bold;
            }}

            .key {{
                margin-top: 20px;
                font-size: 26px;
                font-weight: bold;
                word-break: break-all;
            }}

            .banner {{
                width: 100%;
                max-width: 728px;
                min-height: 100px;
                margin: 30px auto;
            }}
        </style>
    </head>

    <body>

        <div class="success">
            ✅ KEY BERHASIL<br>
            DIVERIFIKASI
        </div>

        <div class="key">
            {kode}
        </div>

        <div class="banner">

            <div
                id="clikerads-banner"
                data-code="2BF04D80">
            </div>

        </div>

        <script
            src="https://clikerads.com/banner.js"
            async>
        </script>

        <p>
            Key berlaku selama 1 jam.
        </p>

    </body>
    </html>
    """


# ==========================================
# VALIDATE KEY
# ==========================================

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