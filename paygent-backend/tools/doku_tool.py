import os
import httpx
import json
import uuid
import datetime

from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool
def create_doku_payment_link(nama_klien: str, item_deskripsi: str, nominal_rupiah: int) -> str:
    """Gunakan tool ini untuk membuat payment link Doku ketika user meminta untuk menagih seseorang. Input adalah nama_klien (string), item_deskripsi (string), dan nominal_rupiah (integer)."""
    client_id = os.getenv("DOKU_CLIENT_ID")
    secret_key = os.getenv("DOKU_SECRET_KEY")
    base_url = os.getenv("DOKU_BASE_URL")

    invoice_number = f"INV-{str(uuid.uuid4()).replace('-', '').upper()[:8]}"

    body = {
        "order": {
            "amount": nominal_rupiah,
            "invoice_number": invoice_number,
            "currency": "IDR",
            "session_id": str(uuid.uuid4()),
        },
        "payment": {
            "payment_due_date": 60,
        },
        "customer": {
            "name": nama_klien,
            "email": "billing@paygent.ai",
        },
        "line_items": [
            {
                "id": "ITEM-001",
                "name": item_deskripsi,
                "price": nominal_rupiah,
                "quantity": 1,
            }
        ],
    }

    headers = {
        "Client-Id": client_id,
        "Request-Id": str(uuid.uuid4()),
        "Request-Timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Signature": f"HMACSHA256={secret_key}",
        "Content-Type": "application/json",
    }

    try:
        response = httpx.post(
            f"{base_url}/checkout/v1/payment",
            headers=headers,
            json=body,
            timeout=30,
        )

        if response.status_code == 200:
            response_json = response.json()
            return response_json["response"]["payment"]["url"]
        else:
            return f"ERROR: Doku API mengembalikan status {response.status_code}. Detail: {response.text}"
    except httpx.RequestError as e:
        return f"ERROR: Gagal terhubung ke Doku API. Periksa koneksi internet. Detail: {str(e)}"
    except KeyError:
        return "ERROR: Struktur response Doku tidak dikenal. Payment link tidak ditemukan dalam response."
