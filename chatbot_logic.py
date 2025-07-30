import httpx
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

API_KEY = os.getenv("GROQ_API")

LOG_FILE = "token_usage.log"

def log_token_usage(tokens_used: int):
    now = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{now} - Tokens used: {tokens_used}\n")

async def get_ai_reply(message: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://example.com",
        "X-Title": "Chatbot Sederhana",
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "Kamu adalah asisten AI yang membantu menjawab pertanyaan pengguna, baik mudah ataupun kompleks. Berikan jawaban yang ramah dan jelas. Gunakan bahasa Indonesia."},
            {"role": "user", "content": message}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
            res.raise_for_status()
            result = res.json()
            
            # Ambil total token yang dipakai dari response
            usage = result.get("usage", {})
            total_tokens = usage.get("total_tokens", 0)
            
            # Log token usage
            log_token_usage(total_tokens)
            
            return result["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        print("HTTP error:", e.response.status_code, e.response.text)
        return "Maaf, terjadi kesalahan dari server."
    except Exception as e:
        print("Unexpected error:", str(e))
        return "Maaf, ada masalah pada sistem kami."
