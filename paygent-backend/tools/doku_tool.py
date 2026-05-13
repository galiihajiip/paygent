"""
Doku Payment Gateway Tool
Handles payment link creation via Doku Checkout API (sandbox).
"""

import hashlib
import hmac
import uuid
import json
from datetime import datetime, timezone, timedelta
from os import environ

import httpx
from dotenv import load_dotenv

load_dotenv()

DOKU_CLIENT_ID = environ.get("DOKU_CLIENT_ID", "")
DOKU_SECRET_KEY = environ.get("DOKU_SECRET_KEY", "")
DOKU_BASE_URL = environ.get("DOKU_BASE_URL", "https://api-sandbox.doku.com")


def _generate_signature(client_id: str, request_id: str, request_target: str, digest: str, timestamp: str) -> str:
    """Generate HMAC-SHA256 signature for Doku API authentication."""
    component = f"Client-Id:{client_id}\nRequest-Id:{request_id}\nRequest-Timestamp:{timestamp}\nRequest-Target:{request_target}\nDigest:{digest}"
    signature = hmac.new(
        DOKU_SECRET_KEY.encode("utf-8"),
        component.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"HMACSHA256={signature}"


def _generate_digest(body: dict) -> str:
    """Generate SHA-256 digest of request body."""
    import base64
    body_str = json.dumps(body, separators=(",", ":"))
    hash_value = hashlib.sha256(body_str.encode("utf-8")).digest()
    return base64.b64encode(hash_value).decode("utf-8")


async def create_payment_link(
    amount: int,
    customer_name: str,
    customer_email: str,
    order_id: str | None = None,
    item_name: str = "Payment",
) -> dict:
    """
    Create a Doku checkout payment link.

    Args:
        amount: Payment amount in IDR (integer).
        customer_name: Full name of the customer.
        customer_email: Email of the customer.
        order_id: Optional custom order ID. Auto-generated if not provided.
        item_name: Description of the item/service.

    Returns:
        dict with payment_url, order_id, and amount on success,
        or error details on failure.
    """
    if not order_id:
        order_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"

    request_target = "/checkout/v1/payment"
    request_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    body = {
        "order": {
            "amount": amount,
            "invoice_number": order_id,
            "currency": "IDR",
            "session_id": request_id,
        },
        "payment": {
            "payment_due_date": 60,
        },
        "customer": {
            "id": str(uuid.uuid4()),
            "name": customer_name,
            "email": customer_email,
        },
        "item_details": [
            {
                "name": item_name,
                "price": amount,
                "quantity": 1,
            }
        ],
    }

    digest = _generate_digest(body)
    signature = _generate_signature(DOKU_CLIENT_ID, request_id, request_target, digest, timestamp)

    headers = {
        "Content-Type": "application/json",
        "Client-Id": DOKU_CLIENT_ID,
        "Request-Id": request_id,
        "Request-Timestamp": timestamp,
        "Signature": signature,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DOKU_BASE_URL}{request_target}",
            json=body,
            headers=headers,
            timeout=30.0,
        )

    if response.status_code in (200, 201):
        data = response.json()
        return {
            "success": True,
            "payment_url": data.get("response", {}).get("payment", {}).get("url", ""),
            "order_id": order_id,
            "amount": amount,
            "customer_name": customer_name,
            "customer_email": customer_email,
        }
    else:
        return {
            "success": False,
            "error": response.text,
            "status_code": response.status_code,
        }


async def check_payment_status(order_id: str) -> dict:
    """
    Check payment status for a given order ID via Doku API.

    Args:
        order_id: The invoice/order number to check.

    Returns:
        dict with payment status information.
    """
    request_target = f"/orders/v1/status/{order_id}"
    request_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # GET requests have empty body digest
    empty_digest = _generate_digest({})
    signature = _generate_signature(DOKU_CLIENT_ID, request_id, request_target, empty_digest, timestamp)

    headers = {
        "Content-Type": "application/json",
        "Client-Id": DOKU_CLIENT_ID,
        "Request-Id": request_id,
        "Request-Timestamp": timestamp,
        "Signature": signature,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DOKU_BASE_URL}{request_target}",
            headers=headers,
            timeout=30.0,
        )

    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "order_id": order_id,
            "status": data.get("transaction", {}).get("status", "UNKNOWN"),
            "details": data,
        }
    else:
        return {
            "success": False,
            "error": response.text,
            "status_code": response.status_code,
        }
