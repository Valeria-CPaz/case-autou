from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Permite requisiçõs de qualquer frontend durante o desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API do case AutoU funcionando! 🚀"}

@app.post("/process_email")
async def process_email(
    email_file: UploadFile = File(None),
    email_text: str = Form(None)
):
    #Validação básica
    if not email_file and not email_text:
        return {"error": "Envie um arquivo ou texto!"}
    
    # Lê o conteúdo do arquivo se foi enviado
    text_content = ""
    if email_file:
        filename = email_file.filename.lower()
        contents = await email_file.read()
        if filename.endswith(".txt"):
            text_content = contents.decode("utf-8", errors = "ignore")
        elif filename.endswith(".pdf"):
            text_content = "=== TODO ==="
        else:
            return {"error": "Formato de arquivo não suportado."}
    elif email_text:
        text_content = email_text    

    return {
        "status": "ok",
        "original_text": text_content[:1000] # Limitação para não explodir resposta
    }