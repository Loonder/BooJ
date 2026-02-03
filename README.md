# 👻 BooJ - Caçador Inteligente de Vagas

<div align="center">

![BooJ Logo](assets/boo_ghost_clean.png)

**Agregador inteligente de vagas para estágios em TI com scraping paralelo e dashboard moderno**

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/Loonder/BooJ/test.yml?branch=main&label=tests&logo=github)](https://github.com/Loonder/BooJ/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Demo](#-demo) • [Features](#-features) • [Quick Start](#-quick-start) • [Tech Stack](#-tech-stack) • [Contributing](CONTRIBUTING.md)

</div>

---

## 📖 Sobre

**BooJ** é um agregador inteligente de vagas de estágio em TI que:
- 🔍 Coleta vagas de **20+ plataformas** (LinkedIn, Indeed, GitHub, Gupy, etc)
- ⚡ Scraping **paralelo** (5-10x mais rápido)
- 🌙 Dashboard **moderno** com Next.js 14 e dark mode
- 🎯 **Score inteligente** baseado em relevância
- 📊 Métricas com **Prometheus** + logs estruturados
- 🔒 **Seguro** - sem credenciais expostas

**Score do Projeto:** 8.0/10 🎯

---

## ✨ Features

### Backend (Python + FastAPI)
- ✅ **Multi-platform scraping** - LinkedIn, Indeed, ZipRecruiter via [JobSpy](https://github.com/cullenwatson/JobSpy)
- ✅ **Scraping paralelo** - Até 16 workers simultâneos  
- ✅ **Filtros inteligentes** - Remove spam e duplicatas
- ✅ **Score de relevância** - Algoritmo customizado
- ✅ **API REST** - Endpoints `/api/v1/jobs` e `/api/v1/stats`
- ✅ **Observabilidade** - Prometheus metrics + structlog
- ✅ **Banco SQLite** - Leve e sem setup

### Frontend (Next.js 14 + TypeScript)
- ✅ **Dark mode** - Sistema + manual toggle
- ✅ **Mobile-first** - Totalmente responsivo
- ✅ **Filtros avançados** - Por localização (SP, RJ, Remoto) e plataforma
- ✅ **UI moderna** - shadcn/ui + Tailwind CSS
- ✅ **Mascote animado** - Boo flutuando como fantasma 👻
- ✅ **Real-time stats** - Total de vagas e filtradas

### DevOps & Quality
- ✅ **CI/CD** - GitHub Actions rodando testes
- ✅ **Testes** - Pytest com 6 testes passando
- ✅ **Linting** - (em configuração)
- ✅ **Docker** - docker-compose.yml pronto
- ✅ **Segurança** - Auditoria completa realizada

---

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/Loonder/BooJ.git
cd BooJ
```

### 2. Backend Setup
```bash
# Criar ambiente virtual
python -m venv venv311
.\venv311\Scripts\activate  # Windows
source venv311/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas API keys (opcional para teste)
```

### 3. Frontend Setup
```bash
cd jobpulse-dashboard
npm install
```

### 4. Rodar Localmente

**Terminal 1 - Backend API:**
```bash
python -m uvicorn api.main:app --reload --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd jobpulse-dashboard
npm run dev
```

**Terminal 3 - Scraper (opcional):**
```bash
python src/hunter.py
```

Acesse: **http://localhost:3000** 🎉

---

## 📸 Demo

### Dashboard Dark Mode
![Dashboard Screenshot](assets/dashboard_preview.png)
*Dashboard moderno com filtros avançados e dark mode*

### Features em Destaque
- 🏠 **Filtro Remoto** - Apenas vagas remotas
- 📍 **Filtros Regionais** - SP, RJ, MG, Sul, Nordeste, Brasil
- 🔍 **Busca Inteligente** - Por vaga, empresa ou tecnologia
- 🎯 **Ordenação** - Por score, data ou empresa
- 🌙 **Dark/Light Mode** - Troca instantânea

---

## 🏗️ Tech Stack

### Backend
- **Python 3.11** - Linguagem principal
- **FastAPI** - API REST moderna
- **SQLite** - Banco de dados leve
- **JobSpy** - Scraping multi-plataforma
- **BeautifulSoup4** - HTML parsing
- **Selenium** - Scraping dinâmico
- **Structlog** - Logging estruturado
- **Prometheus** - Métricas

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Componentes
- **Lucide Icons** - Ícones
- **next-themes** - Dark mode

### DevOps
- **GitHub Actions** - CI/CD
- **Pytest** - Testes backend
- **Docker** - Containerização
- **Caddy** - Reverse proxy

---

## 📁 Estrutura do Projeto

```
BooJ/
├── src/                    # Backend Python
│   ├── hunter.py          # Scraper principal
│   ├── database.py        # Gerenciamento SQLite
│   ├── intelligence.py    # Score e filtros
│   ├── scraper_*.py       # Scrapers específicos
│   └── metrics.py         # Prometheus
│
├── api/                    # FastAPI
│   ├── main.py            # Endpoints REST
│   └── requirements.txt
│
├── jobpulse-dashboard/    # Next.js Frontend
│   ├── app/               # Pages e layouts
│   ├── components/        # React components
│   └── types/             # TypeScript types
│
├── tests/                 # Testes
├── .github/workflows/     # CI/CD
└── data/                  # Database (gitignored)
```

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente (.env)

```bash
# APIs (opcional - JobSpy funciona sem)
JOOBLE_API_KEY=your_key_here
TELEGRAM_TOKEN=your_bot_token

# Notificações (opcional)
TELEGRAM_CHAT_ID=your_chat_id

# Scraping
MAX_WORKERS=16  # Paralelismo
```

### Rodar com Docker

```bash
docker-compose up
```

### Rodar Testes

```bash
# Backend
pytest

# Com coverage
pytest --cov=src

# Frontend (quando implementado)
cd jobpulse-dashboard
npm test
```

---

## 📊 Métricas e Monitoramento

### Prometheus Metrics
Acesse: http://localhost:8000/metrics

Métricas disponíveis:
- `jobs_scraped_total` - Total de vagas coletadas
- `scrape_duration_seconds` - Tempo de scraping
- `scrape_errors_total` - Erros durante scraping

### Logs Estruturados
Logs em JSON com structlog para fácil parsing.

---

## 🤝 Contributing

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

### Como Contribuir
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/amazing`)
3. Commit suas mudanças (`git commit -m '✨ Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing`)
5. Abra um Pull Request

---

## 🐛 Issues & Support

Encontrou um bug? Tem uma sugestão?
- [Abra uma issue](https://github.com/Loonder/BooJ/issues)
- Descreva o problema claramente
- Inclua screenshots se possível

---

## 📝 Roadmap

- [ ] Deploy público (Vercel + Railway)
- [ ] Notificações por email
- [ ] Export para CSV/PDF
- [ ] Testes frontend
- [ ] Real-time updates (SSE)
- [ ] Autenticação de usuários
- [ ] Vagas favoritas/salvas

---

## 📜 License

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Paulo Moraes**

- 🌐 Portfolio: [paulomoraes.cloud](https://paulomoraes.cloud)
- 💼 LinkedIn: [paulomoraesdev](https://linkedin.com/in/paulomoraesdev)
- 🐙 GitHub: [Loonder](https://github.com/Loonder)

---

## ☕ Apoie o Projeto

Esse projeto te ajudou? Considere ajudar a mantê-lo! ❤️

**Pix (Celular):** `11941068987`

---

## 🙏 Agradecimentos

- [JobSpy](https://github.com/cullenwatson/JobSpy) - Biblioteca de scraping
- [shadcn/ui](https://ui.shadcn.com/) - Componentes UI
- [FastAPI](https://fastapi.tiangolo.com/) - Framework Python

---

<div align="center">

**Feito com 👻 por Paulo Moraes**

⭐ Se este projeto te ajudou, dê uma estrela!

</div>
