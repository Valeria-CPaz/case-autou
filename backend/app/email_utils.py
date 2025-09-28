import PyPDF2
from io import BytesIO
import spacy
import os
import google.generativeai as genai
from dotenv import load_dotenv


def extract_text_from_file(filename: str, contents: bytes) -> str:
    """
    Extrai o texto do arquivo (txt ou pdf)
    Usei essa abordagem para permitir uploads diretos do front
    Args: filename - Nome do arquivo
          contents - conteúdo bruto do arquito (bytes)
    Returns: str - texto extraído (ou msg de erro)    
    """
    filename = filename.lower()
    if filename.endswith(".txt"):
        # Decodifica arquito TXT
        return contents.decode("utf8", errors="ignore")
    elif filename.endswith(".pdf"):
        # Extrai texto do PDF
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(contents))
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() or ""
            return text_content
        except Exception as e:
            # Em caso de erro
            return f"[ERRO PDF] {e}"
    else:
        # Extensão de arquivo não suportada
        return None


# Carrega o modelo spaCy para português
nlp = spacy.load("pt_core_news_sm")


def preprocess_text(text: str) -> str:
    """
    Pré-processamento usando spaCy: remove stopwords, pontuação e faz lematização
    Isso aumenta a precisão dos classificadores e reduz ruído
    Args: text - texto de entrada
    Returns: str - texto limpo e pré-processado
    """
    doc = nlp(text)
    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(tokens)


# Classificação com Gemini (2.5-flash)
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)

def classify_and_reply_gemini(text: str) -> dict:
    """
    Integração com a Google Gemini para classificação e sugestão de resposta
    Retorna resultado em formato padronizado esperado pelo front
    Args: text - texto pré-processado
    Returns: dict -
    """
    prompt = (
        "Você é um assistente para uma equipe que recebe muitos e-mails.\n"
        "Classifique o e-mail abaixo como 'Produtivo' ou 'Improdutivo' e sugira uma resposta automática adequada para a categoria.\n"
        "Retorne exatamente neste formato (em português):\n"
        "Categoria: <Produtivo/Improdutivo>\n"
        "Resposta: <resposta automática>\n\n"
        f"E-mail:\n{text}"
    )

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        output = response.text
        categoria = "Desconhecido"
        resposta = ""
        for line in output.split("\n"):
            if line.lower().startswith("categoria:"):
                categoria = line.split(":", 1)[-1].strip()
            if line.lower().startswith("resposta:"):
                resposta = line.split(":", 1)[-1].strip()
        return {"categoria": categoria, "resposta": resposta}
    except Exception as e:
        return {"categoria": "Erro", "resposta": f"Erro ao usar Gemini: {e}"}


# Classificador Fallback
def classify_and_reply(text: str) -> dict:
    """
    Classificação local baseada em palavras-chaves 
    Serve como fallback caso a IA externa esteja fora ou exceda timeout
    """
    texto = text.lower()
    
    produtivas = [
    "problema", "suporte", "atualização", "erro", "senha", "dúvida",
    "requisição", "pedido", "cadastro", "sistema", "login",
    "travar", "bug", "acesso", "pagamento", "reembolso",
    "cancelamento", "ajuda", "documento", "formulário", "falha",
    "conta", "registro", "plataforma", "atendimento", "reclamação"
]

    improdutivas = [
    "feliz", "parabéns", "obrigado", "agradeço", "bom dia",
    "boa tarde", "boa noite", "abraço", "saudade",
    "boa sorte", "agradecimento", "elogio", "comemorar",
    "festas", "felicidades", "cumprimentos"
]
    if any(p in texto for p in produtivas):
        categoria = "Produtivo"
        resposta = "Mensagem classificada como produtiva. Em breve daremos retorno sobre sua solicitação."
    elif any(i in texto for i in improdutivas):
        categoria = "Improdutivo"
        resposta = "Mensagem classificada como improdutiva. Não é necessário responder."
    else:
        categoria = "Produtivo"
        resposta = "Mensagem registrada. Caso necessário, entraremos em contato."

    return {"categoria": categoria, "resposta": resposta}


