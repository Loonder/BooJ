import asyncio
from telegram import Bot
from telegram.error import TelegramError
import logging

try:
    from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
except ImportError:
    TELEGRAM_TOKEN = None
    TELEGRAM_CHAT_ID = None

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.enabled = bool(self.token and self.chat_id and self.token != "SEU_TOKEN_AQUI")

    async def send_message_async(self, message: str):
        if not self.enabled:
            return
            
        try:
            bot = Bot(token=self.token)
            await bot.send_message(chat_id=self.chat_id, text=message, parse_mode='Markdown')
            logger.info("📢 Notificação Telegram enviada com sucesso.")
        except Exception as e:
            logger.error(f"❌ Erro ao enviar Telegram: {e}")

    def send_job_alert(self, job):
        """Dispara alerta de nova vaga."""
        if not self.enabled: return

        msg = (
            f"🚀 **Nova Vaga Encontrada!**\n\n"
            f"💼 **{job['titulo']}**\n"
            f"🏢 {job['empresa']}\n"
            f"📍 {job['localizacao']}\n"
            f"🔗 [Ver Vaga]({job['link']})\n\n"
            f"🎯 Score: {job.get('score', 'N/A')}/100\n"
            f"#{job['plataforma'].replace(' ', '')}"
        )
        
        # Executar async em contexto sincrono
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_message_async(msg))
        loop.close()

    def send_daily_summary(self, jobs):
        """Envia um resumo diário."""
        if not self.enabled or not jobs: return
        
        top_jobs = sorted(jobs, key=lambda x: x.get('score', 0), reverse=True)[:5]
        
        msg = f"📊 **Resumo JobPulse**\n\nForam encontradas {len(jobs)} vagas hoje.\n\n🔥 **Top 5 Melhores Matches:**\n"
        
        for i, job in enumerate(top_jobs, 1):
            msg += f"{i}. [{job['titulo']}]({job['link']}) - {job['empresa']} ({job.get('score')}pts)\n"
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_message_async(msg))
        loop.close()
