# JobSpy Integration - Checklist

## ✅ Backup Criado
- backup_20260202_175748/

## 📥 Download Python 3.11
**Link**: https://www.python.org/downloads/release/python-3119/
- Escolher: "Windows installer (64-bit)"
- ✅ MARCAR: "Add Python 3.11 to PATH"

## ⚙️ Setup Steps

### 1. Executar Setup
```batch
setup_python311.bat
```

### 2. Testar JobSpy
```batch
venv311\Scripts\activate
python test_jobspy.py
```

**Resultado esperado:**
```
✅ JobSpy importado com sucesso!
🔍 Buscando vagas...
✅ Total: 10-20 vagas encontradas!
```

### 3. Integrar no Hunter

Arquivo já criado: `src/scraper_jobspy_real.py`

Adicionar no `src/hunter.py`:

**No topo (imports):**
```python
from scraper_jobspy_real import JobSpyRealScraper
```

**No run_cycle() (após linha 188):**
```python
# 17. JobSpy (LinkedIn + Indeed + ZipRecruiter) **PYTHON 3.11**
try:
    logger.info("🌐 Caçando via JobSpy (Multi-Platform)...")
    jobspy = JobSpyRealScraper()
    raw_jobs.extend(jobspy.fetch_jobs(SEARCH_TERMS))
except Exception as e: 
    logger.error(f"Erro JobSpy: {e}")
```

**Atualizar source count (linha 62):**
```python
logger.info("=== 🚀 INICIANDO CICLO DE CAÇA (16 FONTES DE QUALIDADE) ===")
```

### 4. Teste Final
```batch
start_with_venv.bat
```

## 🎯 Resultado Esperado

| Fonte | Vagas |
|-------|-------|
| JobSpy (LinkedIn) | 80-120 |
| JobSpy (Indeed) | 80-120 |
| JobSpy (ZipRecruiter) | 40-60 |
| Gupy | 100-200 |
| Reddit | 50-100 |
| Telegram | 30-50 |
| Catho | 30-50 |
| Trampo.co | 20-30 |
| Outros 11 | 100 |
| **TOTAL** | **700-900** 🚀 |

## ⚠️ Troubleshooting

Se JobSpy falhar:
- Verificar venv ativo: `python --version` → 3.11.x
- Reinstalar: `pip install -U python-jobspy`
- Checar logs: `logs/hunter.log`

## 🔄 Rollback

Se algo der errado:
```batch
# Restaurar backup
xcopy /E /I /H /Y backup_20260202_175748\* .
```

---

**Status**: ⏳ Aguardando Download Python 3.11
