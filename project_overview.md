# 👻 BooJ System - Visão Geral do Projeto

## 🎯 O Que É?
O **BooJ System (códinome: JobPulse)** é uma plataforma avançada de inteligência para encontrar estágios em TI. Diferente de agregadores comuns, ele atua como um "Caçador Autônomo" (Hunter Bot) que varre a internet 24/7, filtra vagas ruins, pontua as boas e te avisa onde você estiver.

---

## 🚀 Roadmap Executado (Status: Online)

Aqui está tudo o que foi construído e está rodando no seu VPS:

### 1. Fontes de Vagas (O "Ouvido" do Sistema)
O sistema monitora **8 fontes diferentes** simultaneamente:
- [x] **Indeed Brasil**: Com motor browser para simular humano.
- [x] **LinkedIn Stealth**: Modo "espião" (sem login) e modo autenticado.
- [x] **GitHub Jobs**: Monitora issues de repositórios de vagas.
- [x] **RemoteOK**: Monitora API de vagas remotas.
- [x] **Google Kenoby**: Hack (Dork) para achar vagas da Kenoby indexadas.
- [x] **Gupy Hunter**: Hack para achar vagas da Gupy via Google.
- [x] **X (Twitter)**: Monitora tweets recentes de vagas.
- [x] **Sniper Mode**: Sites menores (Programathor, Trampos, etc).

### 2. Inteligência (O "Cérebro")
Não apenas coleta, ele processa:
- [x] **Filtro Anti-Lixo**: Remove vagas sênior/pleno disfarçadas.
- [x] **Match de Skills**: Pontua vagas (0-100) baseado no seu perfil (Python, Dev, etc).
- [x] **Deduplicação Inteligente**: Usa *Fuzzy Matching* para saber se "Dev Python" na Gupy é a mesma vaga que "Desenvolvedor Python" no LinkedIn.
- [x] **Badges**: Classifica automaticamente (Ouro, Prata, Lixo).

### 3. Notificações (A "Voz")
- [x] **Telegram Bot**: Te manda as "Top Vagas" (>40pts) na hora.
- [x] **Discord Webhook**: Canal de log com todas as vagas encontradas.

### 4. Interface (A "Cara")
- [x] **Dashboard Streamlit**: Painel web acessível no seu navegador.
- [x] **Analytics**: Gráficos de tecnologias em alta.
- [x] **Botão de Doação**: Integração PayPal/Pix.
- [x] **Radar de Skills**: Gráfico aranha com demanda de mercado.

### 5. Infraestrutura (O "Corpo")
- [x] **VPS Linux**: Hospedagem profissional.
- [x] **Docker & Compose**: Containerização (roda igual em qualquer lugar).
- [x] **Segurança**: Variáveis de ambiente (.env) protegidas.

---

## 🛠️ Tecnologias Usadas
*   **Linguagem**: Python 3.10+
*   **Web Scraper**: Selenium, Undetected Chromedriver, BeautifulSoup4, Requests.
*   **Data Science**: Pandas, FuzzyWuzzy, Plotly.
*   **Frontend**: Streamlit.
*   **Deploy**: Docker, Nginx (Reverse Proxy).

---

## 🔮 O Que Vem Por Aí? (Futuro)
*   [ ] **Auto-Apply**: Robô que aplica para as vagas sozinho (Fase 15 - Complexo).
*   [ ] **IA Generativa**: Usar GPT para escrever cartas de apresentação para cada vaga.
*   [ ] **App Mobile**: Transformar o dashboard em PWA.

---

**Status Final:** Entregue, Testado e Operacional. 👻✅
