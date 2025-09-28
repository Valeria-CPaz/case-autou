import { useState, useEffect } from "react";
import produtivoImg from "./assets/produtivo.png";
import improdutivoImg from "./assets/improdutivo.png";
import logo_dark from './assets/logo_dark.png';
import cloud from './assets/cloud.png';
import "./App.css";


const API_KEY = import.meta.env.VITE_API_KEY;


function App() {
  const [emailText, setEmailText] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showCopied, setShowCopied] = useState(false);
  const [theme, setTheme] = useState("light");
  const [analytics, setAnalytics] = useState({
    total: 8,
    produtivos: 4,
    improdutivos: 4,
    fallbacks: 0,
  });


  // Busca stats
  const fetchStats = async () => {
    try {
      const resp = await fetch(`${API_KEY}/stats`);
      const stats = await resp.json();
      setAnalytics(stats);
    } catch (err) {
      console.log("Erro na contagem de stats");
    }
  };

  // Drag & Drop handlers
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  // Lê arquivo como texto (txt/pdf)
  const handleFile = (file) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      setEmailText(e.target.result);
    };
    reader.readAsText(file);
  };

  // Cola texto do clipboard no textarea
  const handlePaste = (e) => {
    setEmailText(e.clipboardData.getData("text"));
  };

  // O handleClassify é o coração do app — envia o email/texto para o backend e atualiza os resultados
  const handleClassify = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_KEY}/process_email`, {
        method: "POST",
        body: new URLSearchParams({ email_text: emailText }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });
      const data = await response.json();
      
      setResult({
        label: data.categoria,
        suggestion: data.resposta_sugerida,
        fonte: data.fonte,
        image: data.categoria === "Produtivo" ? produtivoImg : improdutivoImg,
      });
    } catch (err) {
      setResult({
        label: "Erro",
        suggestion: "Falha ao classificar. Tente novamente.",
      });
    }
    setLoading(false);
    fetchStats(); // Atualiza o contador de analytics
  }

  // Copia sugestão de resposta para clipboard
  const handleCopy = () => {
    if (result?.suggestion) {
      navigator.clipboard.writeText(result.suggestion);
      setShowCopied(true);
      setTimeout(() => setShowCopied(false), 900);
    }
  };

  // Toggle de light/dark mode
  const toggleTheme = () => {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.body.classList.toggle("dark-mode", next === "dark");
  };

  // Atalho: Ctrl+Enter para classificar
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") handleClassify();
  };

  // Busca stats
  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <>
      <main>
        <div className="app-main">

          {/* Light mode | Dark mode */}
          <button className="theme-toggle" onClick={toggleTheme}>
            {theme === "light" ? "🌚" : "🌞"}
          </button>

          {/* Logo central */}
          <a href="https://www.autou.io/" target="_blank"><img src={logo_dark} alt="Logo da AutoU" className="meu-logo" /></a>

          {/* Card central de upload + texto */}
          <div className="central-card">
            <div className="title">Classificador de E-mails</div>

            {/* Área de upload de arquivo */}
            <div className="inputs-row">
              <div
                className={`upload-area${isDragging ? " dragover" : ""}`}
                onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={e => { e.preventDefault(); setIsDragging(false); }}
                onDrop={handleDrop}
                tabIndex={0}
                aria-label="Arraste e solte o arquivo do e-mail aqui"
              >
                <img src={cloud} alt="Cloud upload" className="cloud" />
                <div className="upload-instruction">
                  Arraste e solte seu arquivo aqui!
                  <div className="upload-ou">ou</div>
                </div>
                <input
                  type="file"
                  className="file-input"
                  id="file-upload"
                  accept=".txt,.pdf"
                  onChange={e => handleFile(e.target.files[0])}
                />
                <label
                  htmlFor="file-upload"
                  className="file-label"
                >
                  Selecione um Arquivo 📄
                  <div className="file-types">
                    .txt ou .pdf
                  </div>
                </label>
              </div>

              {/* Área de texto para colar o e-mail */}
              <div className="textarea-area">
                <textarea
                  id="email-text"
                  value={emailText}
                  placeholder="Cole ou digite aqui o texto do e-mail..."
                  onChange={e => setEmailText(e.target.value)}
                  onPaste={handlePaste}
                  onKeyDown={handleKeyDown}
                  aria-label="Texto do e-mail"
                />
                <button
                  className="button-classify"
                  onClick={handleClassify}
                  disabled={!emailText || loading}
                >
                  {loading ? "Classificando..." : "Classificar E-mail"}
                </button>
              </div>
            </div>
          </div>

          {/* Bloco de resultado — Badge + Sugestão */}
          {(loading || result) && (
            <div className="result-row">
              {loading ? (
                <div className="loading-spinner" aria-label="Carregando..."></div>
              ) : (
                <>
                  {result.image && (
                    <img
                      src={result.image}
                      alt={result.label}
                      className="badge-result"
                    />
                  )}
                  <div className="suggested-reply side">
                    {result.suggestion}
                    <button className="copy-btn" onClick={handleCopy}>
                      {showCopied ? "Copiado!" : "Copiar"}
                    </button>
                  </div>
                </>
              )}
            </div>
          )}

          {/* Analytics */}
          <div className="analytics-fixed">
            Total classificados: {analytics.total} |
            <span className="analytics-prod"> Produtivos: {analytics.produtivos}</span> |
            <span className="analytics-improd"> Improdutivos: {analytics.improdutivos}</span>
          </div>

        </div>

        {/* Rodapé */}
        <div className="footer">
          <div className="footer-copy">
            &copy; {new Date().getFullYear()} Case AutoU | <a href="https://github.com/Valeria-CPaz" target="_blank">Valeria Paz</a>
          </div>
        </div>
      </main >
    </>
  );
}

export default App;
