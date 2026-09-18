from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
import random
import time

app = FastAPI()

# Penyimpanan key sementara
KEYS = {}


class Validate(BaseModel):
    key: str


# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {
        "status": "online"
    }


# =========================
# GENERATE KEY
# =========================
@app.get("/generate", response_class=PlainTextResponse)
def generate():

    # Generate 10 digit
    key = "".join(
        str(random.randint(0, 9))
        for _ in range(10)
    )

    # Key berlaku 1 jam
    KEYS[key] = {
        "expired": time.time() + 3600,
        "verified": False
    }

    return f"KEY: {key}"


# =========================
# VERIFY KEY
# =========================
@app.get("/verify", response_class=HTMLResponse)
def verify(kode: str):

    # Cek key
    if kode not in KEYS:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>Error</title>
        </head>

        <body style="
            font-family: Arial;
            text-align: center;
            padding-top: 80px;
        ">

            <h2>❌ KEY TIDAK DITEMUKAN</h2>

        </body>
        </html>
        """

    # Cek expired
    if time.time() > KEYS[kode]["expired"]:

        del KEYS[kode]

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>Expired</title>
        </head>

        <body style="
            font-family: Arial;
            text-align: center;
            padding-top: 80px;
        ">

            <h2>⌛ KEY SUDAH EXPIRED</h2>

        </body>
        </html>
        """

    # Tandai sudah verify
    KEYS[kode]["verified"] = True

    # =========================
    # HALAMAN VERIFY
    # =========================
    return f"""
<!DOCTYPE html>
<html lang="id">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Verify Key</title>

    <style>

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 40px 15px;
            font-family: Arial, sans-serif;
            background: #ffffff;
            text-align: center;
        }}

        .container {{
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
        }}

        .success {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
            line-height: 1.25;
        }}

        .key {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 30px;
            word-break: break-all;
        }}

        .banner {{
            width: 100%;
            max-width: 728px;
            min-height: 100px;
            margin: 30px auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .info {{
            margin-top: 30px;
            font-size: 14px;
            color: #777;
        }}

        @media (max-width: 600px) {{

            body {{
                padding-top: 50px;
            }}

            .success {{
                font-size: 30px;
            }}

            .key {{
                font-size: 25px;
            }}

        }}

    </style>

</head>


<body>

    <div class="container">

        <!-- SUCCESS -->
        <div class="success">
            ✅ KEY BERHASIL<br>
            DIVERIFIKASI
        </div>


        <!-- KEY -->
        <div class="key">
            {kode}
        </div>


        <!-- ================================= -->
        <!-- CLİKER ADS BANNER                  -->
        <!-- ================================= -->

        <div class="banner">

            <div
                id="clikerads-banner"
                data-code="2BF04D80">
            </div>

        </div>


        <!-- CLİKER ADS SCRIPT -->
        <script
            src="https://clikerads.com/banner.js">
        </script>


        <div class="info">
            Key berlaku selama 1 jam.
        </div>

    </div>

</body>

</html>
"""


# =========================
# VALIDATE KEY
# =========================
@app.post("/validate")
def validate(data: Validate):

    key = data.key

    # Key tidak ada
    if key not in KEYS:
        return {
            "success": False,
            "message": "key tidak ditemukan"
        }

    # Key expired
    if time.time() > KEYS[key]["expired"]:

        del KEYS[key]

        return {
            "success": False,
            "message": "expired"
        }

    # Belum verify
    if not KEYS[key]["verified"]:

        return {
            "success": False,
            "message": "belum verify"
        }

    # Valid
    return {
        "success": True,
        "message": "KEY VALID"
    }