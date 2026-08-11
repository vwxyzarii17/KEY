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


@app.get("/generate", response_class=PlainTextResponse)
def generate():

    key = "".join(str(random.randint(0, 9)) for _ in range(10))

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

    # Tandai key sudah diverifikasi
    KEYS[kode]["verified"] = True

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Verify Key</title>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding-top: 60px;
                background: #ffffff;
            }}

            .container {{
                width: 100%;
                max-width: 800px;
                margin: auto;
            }}

            .ad {{
                margin: 30px auto;
                width: 100%;
                max-width: 728px;
            }}

            iframe {{
                display: block;
                width: 728px;
                height: 90px;
                max-width: 100%;
                margin: auto;
                border: 0;
                overflow: hidden;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h2>✅ KEY BERHASIL DIVERIFIKASI</h2>

            <h3>{kode}</h3>

            <!-- 1POP BANNER -->
            <div class="ad">

                <iframe
                    src="https://1pop.online/ad/banner?zone=ZONE_0CBEE4FFE579EC6B&size=728x90"
                    width="728"
                    height="90"
                    frameborder="0"
                    scrolling="no"
                    style="border:0;overflow:hidden;max-width:100%;">
                </iframe>

            </div>

        </div>

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

    if time.time() > KEYS[data.key]["expired"]:
        del KEYS[data.key]

        return {
            "success": False,
            "message": "expired"
        }

    if not KEYS[data.key]["verified"]:
        return {
            "success": False,
            "message": "belum verify"
        }

    return {
        "success": True,
        "message": "KEY VALID"
    }
