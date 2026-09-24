from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.error import BadRequest

from database import SessionLocal
from services.movie_service import get_or_create_user
from models import MoodType

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    user_id = update.effective_user.id
    from models import User
    existing_user = db.query(User).filter_by(telegram_id=user_id).first()
    
    if existing_user:
        db.close()
        await update.message.reply_text("Sei già registrato nella nostra setta bovina! 🐄\n\nUsa /settings per cambiare le tue preferenze, oppure /naviga per esplorare il pascolo.")
        return
        
    get_or_create_user(db, user_id)
    db.close()
    
    welcome_msg = (
        "✨ 🐮 *MOO! Benvenuto nella setta di Cult MOOvie Advisor!* 🐄 ✨\n\n"
        "Sono il tuo Personal Trainer Cinematografico Bovino! 🎬 Il mio scopo non è darti un noioso motore di ricerca, ma farti scoprire le gemme più preziose e i veri 'cult' della storia del cinema. 💎🍿\n\n"
        "🎯 *Come funziona la magia?*\n"
        "1️⃣ Usa il comando /naviga per esplorare il mio pascolo segreto. 🌾\n"
        "2️⃣ Scegli il tuo **Mood** (umore) e il **Tempo** a tua disposizione. ⏳\n"
        "3️⃣ Ti proporrò una 'carta' film alla volta. Puoi **Sceglierla** 🎬, dire che l'hai **Già vista** 👀 (per salire di livello velocemente!), oppure passare avanti ➡️.\n"
        "4️⃣ Usa /skills per vedere il tuo livello di Cinefilia e sbloccare opere d'arte sempre più rare! 🏆📈\n\n"
        "Inizia digitando o cliccando su /naviga ! Dai gas! 🚀"
    )
    keyboard = [
        [InlineKeyboardButton("🍿 Principiante (Tier 1)", callback_data="set_tier_1")],
        [InlineKeyboardButton("🎬 Appassionato (Tier 2)", callback_data="set_tier_2")],
        [InlineKeyboardButton("🧐 Cinefilo Esperto (Tier 3)", callback_data="set_tier_3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=welcome_msg + "\n\n👇 **Seleziona il tuo livello di partenza:**",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def naviga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("☕ Decompressione / Relax", callback_data="mood_DECOMPRESSION")],
        [InlineKeyboardButton("🧨 Catarsi / Adrenalina", callback_data="mood_CATHARSIS")],
        [InlineKeyboardButton("🌌 Ipnotico / Fuga", callback_data="mood_HYPNOTIC")],
        [InlineKeyboardButton("🧠 Introspezione / Riflessione", callback_data="mood_INTROSPECTION")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Non sai cosa guardare stasera? 🍿 Nessun problema!\n\n👇 Scegli il tuo **Umore Attuale** e io andrò a scavare nel mio pascolo per trovarti il film perfetto! MOO! 🐄✨",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_mood_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest:
        pass
    
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

async def handle_set_tier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest:
        pass
    
    import datetime
    tier = int(query.data.split("_")[2])
    
    db = SessionLocal()
    user = get_or_create_user(db, update.effective_user.id)
    
    # Only reset timestamp if the tier actually changed
    if user.current_tier != tier:
        user.current_tier = tier
        user.tier_updated_at = datetime.datetime.utcnow()
        
    db.commit()
    db.close()
    
    keyboard = [
        [InlineKeyboardButton("✅ Sì, includi film più accessibili", callback_data="lowertier_1")],
        [InlineKeyboardButton("❌ No, mostrami SOLO film del mio Tier", callback_data="lowertier_0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"Ottimo! Ho impostato il tuo livello cinefilo al **Tier {tier}**.\n\nVuoi che ti proponga anche film di Tier inferiori al tuo (se presenti), oppure vuoi vedere **SOLO** film del tuo livello attuale?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_lower_tier_pref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest:
        pass
    
    pref = query.data.split("_")[1]
    include_lower = (pref == "1")
    
    db = SessionLocal()
    user = get_or_create_user(db, update.effective_user.id)
    user.include_lower_tiers = include_lower
    db.commit()
    db.close()
    
    await query.edit_message_text("Tutto pronto! Le tue preferenze sono state salvate. Sei pronto a esplorare il pascolo! MOO 🐄\n\nUsa /naviga per iniziare.", parse_mode="Markdown")

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    user = get_or_create_user(db, update.effective_user.id)
    db.close()
    
    keyboard = [
        [InlineKeyboardButton("🍿 Principiante (Tier 1)", callback_data="set_tier_1")],
        [InlineKeyboardButton("🎬 Appassionato (Tier 2)", callback_data="set_tier_2")],
        [InlineKeyboardButton("🧐 Cinefilo Esperto (Tier 3)", callback_data="set_tier_3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=f"Il tuo livello attuale è **Tier {user.current_tier}**.\n\n👇 **Seleziona il tuo nuovo livello di partenza:**",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def rule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = (
        "📜 *I 10 Comandamenti del Cult MOOvie Advisor* 📜\n\n"
        "1️⃣ *Sii Onesto col tuo Mood:* Scegli l'umore che ti rappresenta in questo esatto momento, senza barare. 🧘‍♂️\n"
        "2️⃣ *Scala i Livelli:* Inizi al Tier 1. Più film guardi (e valuti), più la tua barra /skills si riempie, sbloccando i Tier superiori (film d'autore e di nicchia!). 🧗‍♀️📈\n"
        "3️⃣ *Il Feedback è Sacro:* Dopo aver scelto un film, ti chiederò com'è andata. Questo mi aiuta a far crescere il tuo livello cinefilo e a rendermi un bovino felice! 📝❤️\n"
        "4️⃣ *Nessun Rimpianto:* Se un film non ti convince, puoi sempre scartarlo. Non ti verrà riproposto per un bel po'. 🙅‍♂️🚮\n\n"
        "Che il Grande Bovino guidi le tue visioni! 🐄🎬✨"
    )
    await update.message.reply_text(rules_text, parse_mode="Markdown")

def get_start_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("naviga", naviga),
        CommandHandler("settings", settings),
        CommandHandler("rule", rule),
        CommandHandler("rules", rule),
        CallbackQueryHandler(handle_mood_selection, pattern="^mood_"),
        CallbackQueryHandler(handle_set_tier, pattern="^set_tier_"),
        CallbackQueryHandler(handle_lower_tier_pref, pattern="^lowertier_")
    ]
