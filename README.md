🛑 Limitações encontradas e decisões de arquitetura

Durante o desenvolvimento da solução, foi realizado um estudo e teste prático de diversas abordagens para integração de IA, visando classificar e-mails e sugerir respostas automáticas:

1. Tentativas com APIs de IA externas

Foram testadas as seguintes alternativas:

OpenAI GPT (gpt-3.5-turbo):

Problema: Todas as contas gratuitas testadas atingiram o limite de quota, impedindo o uso durante o desenvolvimento e deploy.

Impacto: Qualquer usuário/avaliador que tentar rodar a API sem chave paga receberá erro de quota (“You exceeded your current quota...”).

Google Gemini (API generativeai):

Problema: Limite de quota free extremamente baixo, impossibilitando uso estável até mesmo para protótipos ou testes simples.

Impacto: Falha com erro 429 (“quota exceeded”) mesmo em contas novas.

Hugging Face Inference API:

Problema: Modelos públicos frequentemente ficam fora do ar, retornam 404 ou erros internos (“index out of range”).
Modelos PT-BR de classificação, sentiment analysis ou spam detection testados estavam todos indisponíveis no momento do desenvolvimento (julho/2025).

Impacto: Não há garantia de funcionamento, mesmo para projetos de MVP/demo.
Além disso, a quota free é muito baixa e pode ser consumida rapidamente.

2. Pipeline local com Transformers

Vantagem:
Permite rodar modelos robustos (como BERT ou Bertweet) localmente, sem depender de quota ou de disponibilidade online.
Não há limite de uso, funciona offline e é ideal para demonstrações locais.

Limitação:
A maioria das plataformas de nuvem gratuita (Render, Vercel, Heroku Free, etc) não permite baixar modelos grandes (~400MB+) ou executar tarefas pesadas de IA devido à limitação de RAM, CPU e armazenamento.
Com isso, o deploy público pode não rodar a IA local — apenas ambientes locais de desenvolvimento.

3. Solução adotada para garantir robustez

A arquitetura do sistema foi desenhada para ser plug-and-play:

Toda a integração com IA (OpenAI, Gemini, Hugging Face) está pronta, documentada e testada, bastando descomentar e inserir a chave.

Para garantir estabilidade e evitar bloqueios no deploy público, a versão principal do sistema utiliza classificação local baseada em palavras-chave, sempre funcionando para qualquer usuário, sem dependência de quota ou APIs externas.

Caso seja necessário rodar IA de verdade, basta seguir a documentação do arquivo external_apis.py e executar localmente.

Resumo:
A decisão foi priorizar robustez e experiência do usuário, evitando travamentos causados por limitação de quota gratuita das APIs públicas.
A arquitetura segue pronta para integração real de IA assim que o ambiente e recursos estiverem disponíveis!