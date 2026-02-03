# Python 3.11 Setup Guide

## Quick Start

1. **Download Python 3.11.9**
   - Link: https://www.python.org/downloads/release/python-3119/
   - Choose: "Windows installer (64-bit)"
   - ✅ **IMPORTANTE**: Marque "Add Python 3.11 to PATH" durante instalação

2. **Run Setup Script**
   ```batch
   # Double-click ou execute:
   setup_python311.bat
   ```
   
3. **Test JobSpy**
   ```batch
   venv311\Scripts\activate
   python test_jobspy.py
   ```

4. **Run JobPulse**
   ```batch
   # Opção 1: Script automático
   start_with_venv.bat
   
   # Opção 2: Manual
   venv311\Scripts\activate
   python src/hunter.py
   ```

## Troubleshooting

### "Python 3.11 não encontrado"
- Reinstale Python 3.11
- Marque "Add to PATH"
- Ou use caminho completo: `C:\Python311\python.exe`

### "JobSpy não instala"
- Verifique versão: `python --version` (deve ser 3.11.x)
- Atualize pip: `python -m pip install --upgrade pip`
- Retry: `pip install -U python-jobspy`

### "Erro de import"
- Certifique-se que venv está ativo
- Reinstale requirements: `pip install -r requirements.txt`

## Expected Results

Com Python 3.11 + JobSpy:
- LinkedIn: 100-150 vagas
- Indeed BR: 100-150 vagas  
- ZipRecruiter: 50-100 vagas
- **Total sistema: 700-900 vagas reais!** 🚀
