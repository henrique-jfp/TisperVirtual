from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    return ChatResponse(reply=f"Você perguntou: {request.prompt}")

@app.get("/")
async def root():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API simples...")
    uvicorn.run(app, host="127.0.0.1", port=8000)