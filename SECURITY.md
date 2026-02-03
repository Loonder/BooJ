# 🔒 GUIA DE SEGURANÇA - JobPulse

## ⚠️ NUNCA COMMITAR

### 🚨 Arquivos Críticos (NUNCA no Git!)
- ✅ `.env` e variações - **PROTEGIDO pelo .gitignore**
- ✅ `*.db`, `*.sqlite` - **PROTEGIDO pelo .gitignore**
- ✅ `venv/`, `venv311/` - **PROTEGIDO pelo .gitignore**
- ✅ `logs/` - **PROTEGIDO pelo .gitignore**
- ✅ `__pycache__/` - **PROTEGIDO pelo .gitignore**

### 🔑 Credenciais que Devem Estar no .env
```bash
# .env (NUNCA commitar este arquivo!)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TELEGRAM_BOT_TOKEN=1234567890:ABC...
TELEGRAM_CHAT_ID=-1001234567890
GITHUB_TOKEN=ghp_...
ADZUNA_APP_ID=...
ADZUNA_API_KEY=...
```

### ✅ Como Usar Variáveis de Ambiente

**CERTO** ✅
```python
import os
from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
```

**ERRADO** ❌
```python
# NUNCA FAZER ISSO!
webhook_url = "https://discord.com/api/webhooks/123456..."
```

---

## 📋 Checklist de Segurança

Antes de fazer `git init`, verificar:

- [x] `.gitignore` criado e completo
- [ ] Buscar por credenciais hardcoded
- [ ] Verificar se `.env` existe e está protegido
- [ ] Criar `.env.example` (sem valores reais)
- [ ] Verificar se `*.db` está no gitignore
- [ ] Verificar se `venv/` está no gitignore
- [ ] Verificar se `logs/` está no gitignore

---

## 🔍 Comandos de Verificação

### Buscar credenciais hardcoded
```bash
# Buscar possíveis senhas/tokens no código
grep -r "password.*=" src/
grep -r "token.*=" src/
grep -r "api_key.*=" src/
grep -r "webhook.*https" src/
```

### Testar .gitignore
```bash
# Ver o que seria commitado
git add --dry-run .

# Verificar se .env seria ignorado
git check-ignore .env
```

---

## 🛡️ Proteções Implementadas

### 1. .gitignore Robusto
- 🔒 Credenciais (`.env`, `*.key`, `*.pem`)
- 🗄️ Bancos de dados (`*.db`, `*.sqlite`)
- 🐍 Python (`venv/`, `__pycache__/`)
- 📝 Logs (`logs/`, `*.log`)
- 💻 IDEs (`.vscode/`, `.idea/`)

### 2. Arquivo .env.example
Template sem credenciais reais:
```bash
# .env.example
DISCORD_WEBHOOK_URL=your_webhook_here
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

---

## 🚨 Se Credenciais Vazaram

### Passos Imediatos:
1. **REVOGAR** todas as credenciais expostas
2. **GERAR** novas credenciais
3. **ATUALIZAR** .env local
4. **LIMPAR** histórico do Git:
   ```bash
   # Remover arquivo do histórico
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (CUIDADO!)
   git push origin --force --all
   ```

---

## ✅ Boas Práticas

1. **Sempre** usar variáveis de ambiente
2. **Nunca** hardcodar credenciais
3. **Revisar** cada commit antes de push
4. **Usar** `.env.example` como template
5. **Manter** `.gitignore` atualizado
6. **Rotacionar** credenciais periodicamente

---

## 🔐 Ferramentas Recomendadas

- **git-secrets**: Previne commits de segredos
- **truffleHog**: Busca credenciais no histórico
- **pre-commit hooks**: Validação automática

---

**Status**: 🔒 Protegido!  
**Última verificação**: Auto-verificação antes de cada commit
