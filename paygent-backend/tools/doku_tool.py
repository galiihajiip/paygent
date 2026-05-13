import os
import base64
import hashlib
import hmac
import httpx
import json
import uuid
import datetime

from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


def _build_doku_signature(
    client_id: str,
    secret_key: str,
    request_id: str,
    request_timestamp: str,
    request_target: str,
    body_str: str,
) -> str:
    """Build Doku HMAC-SHA256 signature header value.

    Reference: https://developers.doku.com/getting-started-with-doku-api/signature-component/non-snap/sample-code
    Component format (newline-separated, no trailing newline):
        Client-Id:<client_id>
        Request-Id:<request_id>
        Request-Timestamp:<request_timestamp>
        Request-Target:<request_target>
        Digest:<base64(sha256(body_str))>

    IMPORTANT: body_str must be the EXACT same string sent over the wire.
    Any whitespace difference between digest and actual body invalidates signature.
    """
    digest = base64.b64encode(hashlib.sha256(body_str.encode("utf-8")).digest()).decode("utf-8")

    component = (
        f"Client-Id:{client_id}\n"
        f"Request-Id:{request_id}\n"
        f"Request-Timestamp:{request_timestamp}\n"
        f"Request-Target:{request_target}\n"
        f"Digest:{digest}"
    )

    raw_signature = hmac.new(
        secret_key.encode("utf-8"),
        component.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    signature_b64 = base64.b64encode(raw_signature).decode("utf-8")
    return f"HMACSHA256={signature_b64}"


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
            "line_items": [
                {
                    "id": "ITEM-001",
                    "name": item_deskripsi,
                    "price": nominal_rupiah,
                    "quantity": 1,
                }
            ],
        },
        "payment": {
            "payment_due_date": 60,
        },
        "customer": {
            "id": "PAYGENT-CUST-001",
            "name": nama_klien,
            "email": "billing@paygent.ai",
        },
    }

    request_id = str(uuid.uuid4())
    request_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    request_target = "/checkout/v1/payment"

    # Serialize body ONCE — same exact bytes are used for digest and HTTP request.
    body_str = json.dumps(body, separators=(",", ":"))

    signature = _build_doku_signature(
        client_id=client_id,
        secret_key=secret_key,
        request_id=request_id,
        request_timestamp=request_timestamp,
        request_target=request_target,
        body_str=body_str,
    )

    headers = {
        "Client-Id": client_id,
        "Request-Id": request_id,
        "Request-Timestamp": request_timestamp,
        "Signature": signature,
        "Content-Type": "application/json",
    }

    try:
        response = httpx.post(
            f"{base_url}{request_target}",
            headers=headers,
            content=body_str,
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
