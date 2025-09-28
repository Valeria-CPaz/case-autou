# 🤖 AutoU — Email Classifier Case

Projeto desenvolvido como parte do processo seletivo prático da **AutoU**, focado em automação utilizando Inteligência Artificial.

---

## **Sobre o Projeto**
Sistema web completo para classificar e-mails como “produtivo” ou “improdutivo” com sugestão automática de resposta, usando IA (Google Gemini API com fallback local para maior robustez).

- **Frontend:** React + Vite — Interface simples, responsiva, com suporte a drag & drop de arquivos.
- **Backend:** FastAPI (Python) — Processamento dos uploads, pré-processamento de texto, classificação e sugestão de resposta.

---

## **Deploy Online**
- **Frontend (React/Vite):** [https://case-autou-gray.vercel.app](https://case-autou-gray.vercel.app)
- **Backend (FastAPI):** [https://case-autou-bemf.onrender.com](https://case-autou-bemf.onrender.com)

---

## **Screenshots**
![Tela principal do sistema](images/screenshot_01.png)
![Tela após classificação](images/screenshot_02.png)

## **Como rodar localmente**

### **Pré-requisitos**
- **Python 3.10+** (para o backend)
- **Node.js 18+** (para rodar o frontend com Vite)
- (Recomendado) Ambiente virtual Python: `python -m venv venv`

---

### **1. Backend**
```bash
# Backend
cd backend
python -m venv venv
# Ative o ambiente virtual:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
# Copie .env.example para .env e adicione sua chave da API Gemini
uvicorn app.main:app --reload
```

### **2. Frontend**
```bash
cd frontend
npm install
# Crie um arquivo .env e configure:
VITE_API_URL=http://localhost:8000
npm run dev
```
---

### Observações

- Projeto entregue como case prático para a AutoU.
- A arquitetura está pronta para uso real de IA via Gemini/OpenAI/Hugging Face: basta adicionar sua chave no backend.
- Em ambiente público gratuito, a classificação por IA pode não funcionar sempre devido a limites de quota das APIs.
- Para mais detalhes técnicos, consulte o código e os comentários do projeto.

