from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import run_paygent_agent

app = FastAPI(title="PayGent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    status: str


@app.get("/")
def read_root():
    return {"status": "PayGent API is running", "version": "1.0.0"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(status_code=422, detail="Pesan tidak boleh kosong.")

        reply = run_paygent_agent(request.message)

        if reply.startswith("ERROR:") or reply.startswith("Maaf, terjadi kesalahan"):
            return ChatResponse(reply=reply, status="error")

        return ChatResponse(reply=reply, status="success")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
