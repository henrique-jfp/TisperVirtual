from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import hashlib
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Load .env into environment early so the process has parity with local scripts
load_dotenv()

print("Creating app")
app = FastAPI(title="Tipster API")
print("App created")

# Allow local frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM config (read after .env is loaded)
LLM_BASE = os.environ.get("LLM_BASE", "https://api.groq.com/openai/v1")
LLM_KEY = os.environ.get("LLM_API_KEY", None)
model = os.environ.get("LLM_MODEL", "llama-3.1-8b-instant")

def get_llm_client():
    if LLM_BASE == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=LLM_KEY)
        return genai.GenerativeModel(model)
    else:
        from llm_adapter import GroqClient
        # Se o processo não exportou LLM_API_KEY em env vars, permita que o adapter
        # leia a chave diretamente do `.env` (fallback). Passar None faz o adapter
        # usar seu loader interno que já lê `.env`.
        return GroqClient(api_key=None, base_url=LLM_BASE)

# Documents storage
documents_file = "documents.json"
if os.path.exists(documents_file):
    with open(documents_file, "r") as f:
        documents = json.load(f)
else:
    documents = []

hashes_file = "processed_hashes.json"
if os.path.exists(hashes_file):
    with open(hashes_file, "r") as f:
        processed_hashes = set(json.load(f))
else:
    processed_hashes = set()

def save_documents():
    with open(documents_file, "w") as f:
        json.dump(documents, f)

def save_hashes():
    with open(hashes_file, "w") as f:
        json.dump(list(processed_hashes), f)

class ChatRequest(BaseModel):
    prompt: str
    chat_history: list | None = None

class ChatResponse(BaseModel):
    reply: str

class UploadResponse(BaseModel):
    message: str
    document: dict

@app.get("/api/documents")
async def get_documents():
    return {"documents": documents}

@app.post("/api/chat", response_model=ChatResponse)
async def api_chat(req: ChatRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")
    try:
        if LLM_BASE == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=LLM_KEY)
            model_gemini = genai.GenerativeModel(model)
            response = model_gemini.generate_content(req.prompt)
            reply = response.text
        else:
                from rag_utils import consultar_rag, gerar_resposta_chat, consultar_sqlite_para_partida, gerar_resposta_simples
                # Primeiro, consulta rápida em SQLite para perguntas factuais (placar/resultados)
                sqlite_quick = consultar_sqlite_para_partida(req.prompt)
                if sqlite_quick:
                    # retorno imediato sem chamada ao LLM (muito mais rápido)
                    return {"reply": sqlite_quick}

                contexto = consultar_rag(req.prompt)
                llm_client = get_llm_client()
                # Para prompts curtos, faça uma chamada reduzida e direta (menos tokens, prompt enxuto)
                if len(req.prompt or "") < 120:
                    quick_model = os.environ.get("LLM_QUICK_MODEL", model)
                    reply = gerar_resposta_simples(req.prompt, llm_client, temperature=0.0, max_tokens=160, model=quick_model)
                else:
                    reply = gerar_resposta_chat(req.prompt, contexto, llm_client, chat_history=req.chat_history or [], model=model)
        return {"reply": reply}
    except Exception as e:
        # Log full traceback and exception details to file for debugging
        tb = traceback.format_exc()
        try:
            with open("llm_errors.log", "a", encoding="utf-8") as lf:
                lf.write(f"[{datetime.now().isoformat()}] Exception in /api/chat:\n")
                lf.write(repr(e) + "\n")
                lf.write(tb + "\n\n")
        except Exception:
            pass

        # Return safe error to client but reference the log for full info
        return {"reply": f"Erro na chamada LLM: {str(e)}. Verifique llm_errors.log para detalhes."}
    except Exception as e:
        return {"reply": f"Erro: {str(e)}"}

@app.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), category: str = Form(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        from data_collector import processar_pdf_e_armazenar, armazenar_dados_rag
        contents = await file.read()
        file_hash = hashlib.md5(contents).hexdigest()
        if file_hash in processed_hashes:
            raise HTTPException(status_code=409, detail="Arquivo duplicado.")
        
        ext = file.filename.split('.')[-1].lower()
        if ext in ['pdf']:
            file_type = 'pdf'
        elif ext in ['md']:
            file_type = 'markdown'
        elif ext in ['png', 'jpg', 'jpeg']:
            file_type = 'image'
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")
        
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        if file_type == "pdf":
            processar_pdf_e_armazenar(temp_path, category)
        elif file_type == "markdown":
            armazenar_dados_rag(temp_path, category)
        elif file_type == "image":
            from data_collector import processar_imagem_para_markdown
            markdown_texto = processar_imagem_para_markdown(temp_path)
            if markdown_texto:
                md_temp_path = temp_path.replace(f'.{ext}', '.md')
                with open(md_temp_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_texto)
                armazenar_dados_rag(md_temp_path, category)
                os.remove(md_temp_path)
            else:
                raise HTTPException(status_code=500, detail="Falha ao processar imagem.")
        
        processed_hashes.add(file_hash)
        save_hashes()
        
        doc_id = str(len(documents) + 1)
        new_doc = {
            "id": doc_id,
            "name": file.filename,
            "type": file_type,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "processed"
        }
        documents.append(new_doc)
        save_documents()
        
        os.remove(temp_path)
        
        return {"message": "File uploaded and processed successfully", "document": new_doc}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Running uvicorn")
    uvicorn.run(app, host="127.0.0.1", port=8000)
