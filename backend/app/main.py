from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from .email_utils import (
    extract_text_from_file,
    preprocess_text,
)
from .classifier import classify_with_timeout


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://case-autou-gray.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    """
    Endpoint para processar tanto uploads de arquivos quanto texto colado,
    facilitando uso pela interface web independente do formato
    """

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
    # Pré-processamento de texto para melhorar a acurácia da classificação IA/local
    preprocessed_text = preprocess_text(text_content)

    """
    Classificação e sugestão de resposta
    IA (com fallback e timeout)
    Usei um timeout para evitar travamento caso a IA externa demore,
    caindo para o classificador local se necessário
    """
    ia_result, fonte = classify_with_timeout(text_content, timeout=10)

    # Atualiza contadores para exibir analytics em tempo real na interface
    categoria = str(ia_result.get("categoria", "")).lower()
    if categoria == "produtivo":
        stats["produtivos"] += 1
    elif categoria == "improdutivo":
        stats["improdutivos"] += 1
    if fonte != "gemini":
        stats["fallbacks"] += 1

    # Logs de resultados
    print(
        f"[LOG] Categoria: {ia_result["categoria"]} | Fonte: {fonte} | Texto: {text_content[:60]}..."
    )

    return {
        "status": "ok",
        "fonte": fonte,
        "original_text": text_content[:1000],
        "preprocessed_text": preprocessed_text[:1000],
        "categoria": ia_result["categoria"],
        "resposta_sugerida": ia_result["resposta"],
    }
