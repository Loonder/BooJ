# Deploy Package - Arquivos Essenciais

## 📦 O Que Vai Para Deploy

### Código Fonte (src/)
- ✅ `hunter.py` - Motor principal
- ✅ `database.py` - SQLite DB
- ✅ `filters.py` - Filtros de qualidade
- ✅ `notifier.py` - Discord alerts
- ✅ `notifier_telegram.py` - Telegram alerts
- ✅ Todos os `scraper_*.py` (16 scrapers)

### Configuração
- ✅ `.env` - Variáveis de ambiente
- ✅ `requirements.txt` - Dependências Python
- ✅ `Caddyfile` - Proxy reverso (opcional)
- ✅ `docker-compose.yml` - Container config (opcional)

### Scripts de Startup
- ✅ `setup_python311.bat` - Setup inicial
- ✅ `start_with_venv.bat` - Startup automático

### Data
- ✅ `data/` - Banco de dados SQLite
- ✅ `logs/` - Logs do sistema

### Virtual Environment
- ✅ `venv311/` - Python 3.11 com todas as dependências

---

## ❌ O Que NÃO Vai (Removido)

### Arquivos de Teste
- ❌ `test_*.py` (todos os scripts de teste)
- ❌ `debug*.py/txt`
- ❌ `investigate*.py`
- ❌ `analyze*.py`
- ❌ `stats*.py`
- ❌ `monitor_logs.py`

### Backups
- ❌ `backup_*/` (manter apenas 1 backup recente localmente)
- ❌ `src_backup_*/`
- ❌ `dev_files/`

### Temporários
- ❌ `session*.session`
- ❌ `chat_id.txt`
- ❌ `requirements_temp.txt`
- ❌ `boo.png` (assets não usados)

---

## 🔍 Verificação de Filtros

### Filtros Aplicam em TODAS as Fontes

No `hunter.py` linha 200-210:
```python
# Aplicar filtros em TODAS as vagas coletadas
filtered_jobs = apply_all_filters(raw_jobs)
```

**Confirma**: JobSpy, Gupy, Catho, todas passam pelos mesmos filtros!

**Filtros aplicados:**
1. Remover duplicatas
2. Remover vagas fora do Brasil (se enabled)
3. Remover vagas pleno/senior (só junior/estagio)
4. Validar campos obrigatórios
5. Remover empresas blacklist

---

## 📋 Checklist Pre-Deploy

- [ ] Executar `cleanup_for_deploy.bat`
- [ ] Verificar `.env` configurado
- [ ] Testar `start_with_venv.bat`
- [ ] Confirmar `venv311/` funcional
- [ ] Backup do `data/jobs.db`
- [ ] Zip final ou FileZilla upload

---

## 🚀 Deploy VPS

```bash
# 1. Upload via FileZilla:
#    - src/
#    - requirements.txt
#    - .env
#    - start.sh (criar no servidor)

# 2. No servidor:
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install python-jobspy

# 3. Configurar systemd ou supervisord
sudo nano /etc/systemd/system/jobpulse.service

# 4. Iniciar
sudo systemctl start jobpulse
sudo systemctl enable jobpulse
```

---

## 📊 Tamanho Estimado Deploy

- Código (src/): ~500 KB
- venv311/: ~200 MB
- Data/logs: Variável

**Total**: ~200-250 MB

**Sem venv** (recriar no servidor): ~1 MB 🎯
