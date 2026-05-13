"""
PayGent AI Agent
Uses Google Gemini as the LLM backbone with Doku payment tools.
"""

import json
from os import environ

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.doku_tool import create_payment_link, check_payment_status

load_dotenv()

GOOGLE_API_KEY = environ.get("GOOGLE_API_KEY", "")

client = genai.Client(api_key=GOOGLE_API_KEY)

# Define tools for function calling
PAYMENT_TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="create_payment_link",
                description="Create a payment link for a customer using Doku checkout. Use this when the user wants to pay for something or requests a payment link.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "amount": types.Schema(
                            type=types.Type.INTEGER,
                            description="Payment amount in IDR (Indonesian Rupiah). Must be a positive integer.",
                        ),
                        "customer_name": types.Schema(
                            type=types.Type.STRING,
                            description="Full name of the customer.",
                        ),
                        "customer_email": types.Schema(
                            type=types.Type.STRING,
                            description="Email address of the customer.",
                        ),
                        "order_id": types.Schema(
                            type=types.Type.STRING,
                            description="Optional custom order ID. Will be auto-generated if not provided.",
                        ),
                        "item_name": types.Schema(
                            type=types.Type.STRING,
                            description="Description of the item or service being paid for.",
                        ),
                    },
                    required=["amount", "customer_name", "customer_email"],
                ),
            ),
            types.FunctionDeclaration(
                name="check_payment_status",
                description="Check the payment status of an existing order. Use this when the user asks about the status of their payment.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "order_id": types.Schema(
                            type=types.Type.STRING,
                            description="The order/invoice ID to check status for.",
                        ),
                    },
                    required=["order_id"],
                ),
            ),
        ]
    )
]

SYSTEM_INSTRUCTION = """You are PayGent, a friendly and professional AI payment assistant powered by Doku payment gateway.

Your capabilities:
1. Create payment links for customers (via Doku Checkout API)
2. Check payment status for existing orders

Guidelines:
- Always be polite and helpful
- When a user wants to make a payment, ask for: amount, their name, and email (if not already provided)
- Format currency amounts in IDR (Indonesian Rupiah) with proper formatting (e.g., Rp 100.000)
- After creating a payment link, present it clearly to the user
- If there's an error, explain it in simple terms and suggest next steps
- You can handle casual conversation but always guide users toward payment actions
- Respond in the same language the user uses (Indonesian or English)
"""


async def process_message(user_message: str, conversation_history: list[dict] | None = None) -> str:
    """
    Process a user message through the AI agent.

    Args:
        user_message: The user's input message.
        conversation_history: Optional list of previous messages for context.

    Returns:
        The agent's response string.
    """
    # Build contents from history
    contents = []
    if conversation_history:
        for msg in conversation_history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    # Add current user message
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

    # Call Gemini with tools
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=PAYMENT_TOOLS,
            temperature=0.7,
        ),
    )

    # Handle function calls
    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                fn_name = part.function_call.name
                fn_args = dict(part.function_call.args) if part.function_call.args else {}

                # Execute the tool
                if fn_name == "create_payment_link":
                    result = await create_payment_link(**fn_args)
                elif fn_name == "check_payment_status":
                    result = await check_payment_status(**fn_args)
                else:
                    result = {"error": f"Unknown function: {fn_name}"}

                # Send function result back to model
                contents.append(response.candidates[0].content)
                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=fn_name,
                                response={"result": result},
                            )
                        ],
                    )
                )

                # Get final response
                final_response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        tools=PAYMENT_TOOLS,
                        temperature=0.7,
                    ),
                )

                return final_response.text or "Maaf, saya tidak bisa memproses permintaan Anda saat ini."

    return response.text or "Maaf, saya tidak bisa memproses permintaan Anda saat ini."
