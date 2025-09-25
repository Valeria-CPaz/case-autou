"""
INTEGRAÇÕES COM IA EXTERNA - OpenAI, Gemini e Hugging Face
Deixei este arquivo organizado, cada bloco pronto pra ser usado.
Só descomentar o bloco desejado, inserir a chave e importar no seu projeto.

Testados e verificados em julho/2025. Todos os erros reportados abaixo são reais.
"""

# === 1. OPENAI GPT (https://platform.openai.com/docs/api-reference) ===
# """
# Como usar:
# - Coloque sua chave da OpenAI em .env: OPENAI_API_KEY=sk-xxxxxxx
# - Instale: pip install openai
# - No seu email_utils.py, basta importar essa função e usar no lugar da classificação local!
# - O modelo pode ser alterado para gpt-3.5-turbo ou gpt-4 se tiver chave paga.
#
# Erros encontrados: Limite de quota/free atingido em todas as contas testadas (mensagem: "You exceeded your current quota...").
# """

# import openai
# import os
# from dotenv import load_dotenv
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
#
# def classify_and_reply_openai(text: str) -> dict:
#     prompt = (
#         "Você é um assistente que classifica e-mails como Produtivo ou Improdutivo e sugere resposta automática.\n"
#         "Retorne neste formato:\n"
#         "Categoria: <Produtivo/Improdutivo>\n"
#         "Resposta: <resposta automática>\n\n"
#         f"E-mail:\n{text}"
#     )
#     try:
#         completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#             max_tokens=200,
#         )
#         output = completion.choices[0].message["content"]
#         categoria = "Desconhecido"
#         resposta = ""
#         for line in output.split("\n"):
#             if line.lower().startswith("categoria:"):
#                 categoria = line.split(":", 1)[-1].strip()
#             if line.lower().startswith("resposta:"):
#                 resposta = line.split(":", 1)[-1].strip()
#         return {"categoria": categoria, "resposta": resposta}
#     except Exception as e:
#         return {"categoria": "Erro", "resposta": f"Erro ao usar OpenAI: {e}"}



# === 2. GEMINI (GOOGLE) (https://ai.google.dev/gemini-api/docs/get-started) ===
# """
# Como usar:
# - Gere sua chave em https://aistudio.google.com/app/apikey
# - Adicione ao .env: GEMINI_API_KEY=AIza...
# - Instale: pip install google-generativeai
# - No seu email_utils.py, basta importar essa função e usar.
#
# Erros encontrados: Limite de quota/free tier esgotado em todas as contas testadas.
# """

# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# load_dotenv()
# gemini_key = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=gemini_key)
#
# def classify_and_reply_gemini(text: str) -> dict:
#     prompt = (
#         "Você é um assistente para uma equipe que recebe muitos e-mails.\n"
#         "Classifique o e-mail abaixo como 'Produtivo' ou 'Improdutivo' e sugira uma resposta automática adequada para a categoria.\n"
#         "Retorne exatamente neste formato (em português):\n"
#         "Categoria: <Produtivo/Improdutivo>\n"
#         "Resposta: <resposta automática>\n\n"
#         f"E-mail:\n{text}"
#     )
#     try:
#         model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
#         response = model.generate_content(prompt)
#         output = response.text
#         categoria = "Desconhecido"
#         resposta = ""
#         for line in output.split("\n"):
#             if line.lower().startswith("categoria:"):
#                 categoria = line.split(":", 1)[-1].strip()
#             if line.lower().startswith("resposta:"):
#                 resposta = line.split(":", 1)[-1].strip()
#         return {"categoria": categoria, "resposta": resposta}
#     except Exception as e:
#         return {"categoria": "Erro", "resposta": f"Erro ao usar Gemini: {e}"}



# === 3. HUGGING FACE INFERENCE API (https://huggingface.co/docs/api-inference/index) ===
# """
# Como usar:
# - Gere um token Hugging Face e coloque em .env: HF_API_TOKEN=hf_xxxxxxxx
# - Instale: pip install requests
# - Troque o modelo na url se quiser testar outro (ver links abaixo).
#
# Modelos testados:
# - https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection (404 Not Found)
# - https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis (erro index out of range)
# - https://api-inference.huggingface.co/models/pierreguillou/bert-base-cased-sentiment-analysis-sentibr (fora do ar)
# """

# import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()
# hf_token = os.getenv("HF_API_TOKEN")
# api_url = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection"
# headers = {"Authorization": f"Bearer {hf_token}"}
# payload = {"inputs": text}
# def classify_and_reply_hf(text: str) -> dict:
#     try:
#         response = requests.post(api_url, headers=headers, json=payload, timeout=30)
#         if response.status_code != 200:
#             return {"categoria": "Erro", "resposta": f"Erro Hugging Face: {response.text}"}
#         result = response.json()
#         label_id = result[0]['label'] if isinstance(result, list) else "Desconhecido"
#         if "spam" in label_id.lower():
#             categoria = "Improdutivo"
#             resposta = "Mensagem classificada como improdutiva."
#         elif "ham" in label_id.lower():
#             categoria = "Produtivo"
#             resposta = "Mensagem produtiva."
#         else:
#             categoria = "Desconhecido"
#             resposta = "Não foi possível classificar o e-mail."
#         return {"categoria": categoria, "resposta": resposta}
#     except Exception as e:
#         return {"categoria": "Erro", "resposta": f"Erro ao usar Hugging Face: {e}"}
