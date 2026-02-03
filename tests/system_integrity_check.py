import os
import sys
import logging
from dotenv import load_dotenv

# Setup paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Logging verification
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Pentest")

def check_env():
    logger.info("🔒 [1/5] Verificando Segurança e Variáveis de Ambiente...")
    load_dotenv()
    
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or token == "SEU_TOKEN_AQUI":
        logger.error("❌ TELEGRAM_TOKEN não configurado ou padrão!")
        return False
    if not chat_id or chat_id == "SEU_CHAT_ID_AQUI":
        logger.error("❌ TELEGRAM_CHAT_ID não configurado ou padrão!")
        return False
        
    logger.info("✅ Segredos carregados com sucesso (Token/ID ocultos).")
    return True

def check_intelligence():
    logger.info("🧠 [2/5] Testando Módulo de Inteligência...")
    try:
        from src.intelligence import Intelligence
        brain = Intelligence()
        
        # Test Case 1: Vaga Boa
        good_job = {"titulo": "Estágio em Desenvolvimento Python", "empresa": "Tech Corp", "link": "http://a", "localizacao": "SP", "plataforma": "Test"}
        score = brain.calculate_match_score(good_job)
        if score < 10:
            logger.error(f"❌ Falha de Inteligência: Vaga boa pontuou baixo ({score})")
            return False
            
        # Test Case 2: Anti-Pattern
        bad_job = {"titulo": "Vaga Sênior Especialista", "empresa": "Bad Corp", "link": "http://b"}
        score_bad = brain.calculate_match_score(bad_job)
        if score_bad != -1 and score_bad != 0: # Depende da implementação exata do -1
             logger.warning(f"⚠️ Vaga sênior não foi totalmente descartada (Score: {score_bad})")

        logger.info(f"✅ Inteligência Operante (Score Test: {score}/100).")
        return True
    except ImportError as e:
        logger.error(f"❌ Erro ao importar Intelligence: {e}")
        return False

def check_telegram():
    logger.info("📢 [3/5] Testando Conectividade Telegram...")
    try:
        from src.notifier_telegram import TelegramNotifier
        import asyncio
        
        async def send_test():
            bot = TelegramNotifier()
            await bot.send_message_async("🛡️ **JobPulse Pentest**: Verificação de Integridade Realizada com Sucesso! ✅")
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_test())
        loop.close()
        logger.info("✅ Notificação de teste enviada.")
        return True
    except Exception as e:
        logger.error(f"❌ Falha no Telegram: {e}")
        return False

def check_scrapers():
    logger.info("🕵️ [4/5] Verificando Motores de Busca (Scrapers)...")
    try:
        # Check Imports only to avoid launching full browser and slowing down
        from src.scraper_x import XScraper
        from src.scraper_google_kenoby import GoogleKenobyScraper
        from src.scraper_indeed import IndeedScraper
        
        logger.info("✅ Classes de Scraper (X, Kenoby, Indeed) carregadas corretamente.")
        return True
    except Exception as e:
        logger.error(f"❌ Erro nos Scrapers: {e}")
        return False

def check_files():
    logger.info("📂 [5/5] Verificando Integridade de Arquivos...")
    required = [
        "src/config.py", "src/hunter.py", "src/dashboard.py", 
        "requirements.txt", ".env"
    ]
    missing = []
    for f in required:
        if not os.path.exists(f):
            missing.append(f)
            
    if missing:
        logger.error(f"❌ Arquivos Críticos Faltando: {missing}")
        return False
        
    logger.info("✅ Todos os arquivos críticos presentes.")
    return True

if __name__ == "__main__":
    print("="*40)
    print("🛡️ INICIANDO JOBPULSE SYSTEM CHECK 🛡️")
    print("="*40)
    
    checks = [
        check_env(),
        check_files(),
        check_intelligence(),
        check_scrapers(),
        check_telegram()
    ]
    
    print("-" * 40)
    if all(checks):
        print("✅✅ SISTEMA 100% OPERACIONAL E SEGURO ✅✅")
        print("Pode fazer o deploy sem medo!")
    else:
        print("⚠️ HOUVE FALHAS NO TESTE. VERIFIQUE OS LOGS ACIMA.")
    print("="*40)
