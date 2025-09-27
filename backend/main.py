from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.email_utils import (
    extract_text_from_file,
    preprocess_text,
)
from backend.classifier import classify_with_timeout


app = FastAPI()

# Permite requisiçõs de qualquer frontend durante o desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stats em memória
stats = {
    "total": 0,
    "produtivos": 0,
    "improdutivos": 0,
    "fallbacks": 0,
}


@app.get("/")
def read_root():
    return {"message": "API do case AutoU funcionando! 🚀"}


@app.get("/stats")
def get_stats():
    return stats


@app.post("/process_email")
async def process_email(
    email_file: UploadFile = File(None), email_text: str = Form(None)
):
    # Endpoint que processa o texto (txt, pdf ou texto colado) e retorna o bruto pra etapa de classificação e NLP
    if not email_file and not email_text:
        return {"error": "Envie um arquivo ou texto!"}

    text_content = ""
    if email_file:
        filename = email_file.filename.lower()
        contents = await email_file.read()
        text_content = extract_text_from_file(filename, contents)
        if text_content is None:
            return {"error": "Formato de arquivo não suportado."}

    else:
        text_content = email_text

    # NLP
    preprocessed_text = preprocess_text(text_content)

    # Classificação e sugestão de resposta
    # IA (com fallback e timeout)
    ia_result, fonte = classify_with_timeout(text_content, timeout=7)

    # Atualiza Stats
    stats["total"] += 1
    if ia_result["categoria"].lower() == "produtivo":
        stats["produtivos"] += 1
    elif ia_result["categoria"].lower() == "improdutivo":
        stats["improdutivos"] += 1

    if fonte != "gemini":
        stats["fallbacks"] += 1   

    # Logs de resultados
    print(f"[LOG] Categoria: {ia_result["categoria"]} | Fonte: {fonte} | Texto: {text_content[:60]}...")         

    return {
        "status": "ok",
        "fonte": fonte,
        "original_text": text_content[:1000],
        "preprocessed_text": preprocessed_text[:1000],
        "categoria": ia_result["categoria"],
        "resposta_sugerida": ia_result["resposta"],
    }
