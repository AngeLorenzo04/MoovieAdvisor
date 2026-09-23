from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from database import SessionLocal
from services.movie_service import get_or_create_user
from models import MoodType

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    user_id = update.effective_user.id
    get_or_create_user(db, user_id)
    db.close()
    
    welcome_msg = (
        "🐮 *MOO! Benvenuto nel Cult MOOvie Advisor!* 🐄\n\n"
        "Sono il tuo personal trainer cinematografico bovino. Il mio scopo non è darti un motore di ricerca, ma farti scoprire le gemme più preziose e i 'cult' imperdibili della storia del cinema.\n\n"
        "🎯 *Come funziona?*\n"
        "1. Usa il comando /naviga per esplorare il mio pascolo.\n"
        "2. Scegli il tuo **Mood** e il **Tempo** a disposizione.\n"
        "3. Ti proporrò una 'carta' film alla volta. Puoi sceglierla, dire che l'hai già vista (per incrementare il tuo livello!) o passare oltre.\n"
        "4. Usa /skills per vedere il tuo livello di Cinefilia e sbloccare film più rari!\n\n"
        "Inizia digitando o cliccando su /naviga !"
    )
    
    await update.message.reply_text(
        text=welcome_msg,
        parse_mode="Markdown"
    )

async def naviga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("☕ Decompressione/Conforto", callback_data="mood_DECOMPRESSION")],
        [InlineKeyboardButton("🧨 Catarsi/Adrenalina", callback_data="mood_CATHARSIS")],
        [InlineKeyboardButton("🌌 Ipnotico/Fuga", callback_data="mood_HYPNOTIC")],
        [InlineKeyboardButton("🧠 Introspezione/Profondità", callback_data="mood_INTROSPECTION")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Non sai cosa guardare? Scegli il tuo mood attuale e ti proporrò il film perfetto dal mio pascolo... ehm, archivio storico! MOO!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_mood_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    mood_str = query.data.split("_")[1]
    context.user_data['selected_mood'] = mood_str
    
    keyboard = [
        [InlineKeyboardButton("Meno di 90 min", callback_data="time_90")],
        [InlineKeyboardButton("Tra 90 e 120 min", callback_data="time_120")],
        [InlineKeyboardButton("Oltre 120 min", callback_data="time_999")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"Mood selezionato: *{mood_str}*. MOO! 🐄\n\nQuanto tempo hai a disposizione per brucare questo film?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def get_start_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("naviga", naviga),
        CallbackQueryHandler(handle_mood_selection, pattern="^mood_")
    ]
