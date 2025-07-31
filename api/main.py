from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chatbot_logic import get_ai_reply

app = FastAPI()

# Supaya bisa diakses React (localhost:5173 misalnya)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti ke ['http://localhost:5173'] kalau udah production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def chat(request: Request):
    try:
        body = await request.json()
    except Exception:
        return {"reply": "Bad Request: Harap kirim data dalam format JSON."}

    user_input = body.get("message", [])
    if not user_input:
        return {"reply": "Pesan kosong, mohon masukkan sesuatu."}

    reply = await get_ai_reply(user_input)
    return {"reply": reply}

@app.get("/deploy") 
async def deploy_route():
    return {"message": "Chatbot is running successfully!"}