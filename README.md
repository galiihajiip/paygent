# PayGent - AI Payment Assistant

> AI-powered payment assistant using Doku payment gateway, built for Agenthon.

## Architecture

```
User ↔ Next.js Frontend ↔ FastAPI Backend ↔ Gemini AI Agent ↔ Doku API
```

## Tech Stack

| Layer    | Technology                  |
|----------|-----------------------------|
| Frontend | Next.js 14, Tailwind CSS    |
| Backend  | FastAPI, Python 3.11+       |
| AI       | Google Gemini 2.0 Flash     |
| Payment  | Doku Checkout API (Sandbox) |

## Getting Started

### Backend

```bash
cd paygent-backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# Fill in .env with your credentials
python main.py
```

### Frontend

```bash
cd paygent-frontend
npm install
npm run dev
```

## Features

- 💬 Natural language payment interface
- 💳 Create payment links via Doku Checkout
- 📋 Check payment status
- 🤖 AI-powered conversation with function calling
- 🎨 Clean, responsive chat UI

## Environment Variables

### Backend (.env)
- `DOKU_CLIENT_ID` - Doku sandbox client ID
- `DOKU_SECRET_KEY` - Doku sandbox secret key
- `DOKU_BASE_URL` - Doku API base URL
- `GOOGLE_API_KEY` - Google Gemini API key

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)
