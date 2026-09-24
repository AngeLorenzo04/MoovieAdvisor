import os
import logging
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

from database import init_db
from handlers.start_handler import get_start_handlers
from handlers.session_handler import get_session_handlers
from handlers.profile_handler import get_profile_handlers
from handlers.admin_handler import get_admin_handlers

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token or token == "your_telegram_bot_token_here":
        logging.error("TELEGRAM_BOT_TOKEN non configurato nel file .env!")
        return

    # Inizializza il database se non esiste
    init_db()

    async def post_init(application):
        from telegram import BotCommand
        commands = [
            BotCommand("start", "Avvia o riavvia il bot"),
            BotCommand("skills", "Guarda il tuo livello e i tuoi progressi"),
            BotCommand("popola", "Cerca e aggiungi nuovi film (es. /popola 100)")
        ]
        await application.bot.set_my_commands(commands)

    # Costruisci l'applicazione con il job_queue per la notifica schedulata
    application = ApplicationBuilder().token(token).post_init(post_init).build()

    # Aggiungi gli handler
    for handler in get_start_handlers():
        application.add_handler(handler)
        
    for handler in get_session_handlers():
        application.add_handler(handler)
        
    for handler in get_profile_handlers():
        application.add_handler(handler)
        
    for handler in get_admin_handlers():
        application.add_handler(handler)

    logging.info("Bot in avvio...")
    application.run_polling()

if __name__ == '__main__':
    main()
