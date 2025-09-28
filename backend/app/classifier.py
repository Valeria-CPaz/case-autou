import concurrent.futures
from .email_utils import (
    classify_and_reply,
    classify_and_reply_gemini,
)


def classify_with_timeout(text, timeout=10):
    """
    Usei thread pool para chamar a IA externa (Gemini) com timeout
    Se demorar demais ou der erro, retorna o resultado do classificador local
    """    
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(classify_and_reply_gemini, text)
        try:
            result = future.result(timeout=timeout)
            # Se Gemini retornou erro, também cai pro fallback!
            if not result or "Erro" in result.get("categoria", ""):
                raise Exception("Gemini retornou erro")
            return result, "gemini"
        except Exception as e:
            # Caiu no timeout OU exception OU erro Gemini
            return classify_and_reply(text), "local"
