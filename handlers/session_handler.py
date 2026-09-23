from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.error import BadRequest

from database import SessionLocal
from services.movie_service import get_or_create_user, get_next_movie, log_interaction
from services.job_service import schedule_post_viewing_check
from models import InteractionStatus, FeedbackRating, UserInteraction, MoodType

async def render_movie_card(query, context: ContextTypes.DEFAULT_TYPE, db, user, mood: MoodType, max_time: int, min_time: int = 0):
    movie = get_next_movie(db, user, mood, max_runtime=max_time, min_runtime=min_time)
    
    if not movie:
        msg = "Nessun film trovato in questo pascolo! MOO 🐄 Prova a cambiare filtri o usa /skills per vedere i progressi della tua mandria."
        if query.message.photo:
            await query.message.delete()
            await context.bot.send_message(chat_id=query.message.chat_id, text=msg)
        else:
            await query.edit_message_text(msg)
        return
    
    caption = (
        f"🎬 *{movie.title}* ({movie.year})\n"
        f"👤 Regia: {movie.director} | ⏱ {movie.runtime} min\n"
        f"🏷 Corrente: {movie.movement_tag}\n\n"
        f"⚡ *L'Innovazione:*\n{movie.tech_innovation}\n\n"
        f"🏛️ *L'Eredità:*\n{movie.cultural_legacy}\n\n"
        f"👁️ *Cosa Notare:*\n{movie.watch_tip}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("❌ Passa oltre (Moo...)", callback_data=f"skip_{movie.id}"),
            InlineKeyboardButton("👁️ Già brucato (visto)", callback_data=f"seen_{movie.id}")
        ],
        [
            InlineKeyboardButton("🍿 Scelgo questo! MOO!", callback_data=f"choose_{movie.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        if query.message.photo:
            await query.edit_message_media(
                media=InputMediaPhoto(media=movie.poster_url, caption=caption, parse_mode="Markdown"),
                reply_markup=reply_markup
            )
        else:
            await query.delete_message()
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=movie.poster_url,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
    except BadRequest as e:
        err_msg = str(e)
        if "Failed to get http url content" in err_msg or "Message is not modified" in err_msg or "There is no photo" in err_msg or "Wrong file identifier" in err_msg:
            # Fallback a un messaggio di testo puro se l'immagine non è raggiungibile o non cambia
            if query.message.photo:
                await query.delete_message()
            
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"*(Immagine non disponibile)*\n\n{caption}",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            raise e

async def handle_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest:
        pass
    
    time_limit_str = query.data.split("_")[1]
    max_time = int(time_limit_str)
    min_time = 0
    if max_time == 120:
        min_time = 90
    elif max_time == 999:
        min_time = 120
    
    context.user_data['max_time'] = max_time
    context.user_data['min_time'] = min_time
    
    mood_str = context.user_data.get('selected_mood')
    
    db = SessionLocal()
    user = get_or_create_user(db, update.effective_user.id)
    
    await render_movie_card(query, context, db, user, MoodType(mood_str), max_time, min_time)
    db.close()

async def handle_deck_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest:
        pass
    
    action, movie_id_str = query.data.split("_")
    movie_id = int(movie_id_str)
    
    db = SessionLocal()
    user = get_or_create_user(db, update.effective_user.id)
    
    if action == "skip":
        # Log come skipped o ignora? Il requisito dice "senza penalizzarlo", possiamo loggarlo come SKIPPED
        log_interaction(db, user.id, movie_id, InteractionStatus.SKIPPED)
        
    elif action == "seen":
        log_interaction(db, user.id, movie_id, InteractionStatus.SEEN)
        
    elif action == "choose":
        interaction = log_interaction(db, user.id, movie_id, InteractionStatus.CHOSEN)
        # Schedula job check-in
        movie = db.query(UserInteraction).filter(UserInteraction.id == interaction.id).first().movie
        schedule_post_viewing_check(context, update.effective_user.id, movie.title, movie.runtime, interaction.id)
        
        text_msg = f"🍿 Hai scelto di brucare *{movie.title}*! Buona visione 🐮.\n\nTi contatterò più tardi per un bel MOO di feedback."
        if query.message.photo:
            await query.edit_message_caption(caption=text_msg, parse_mode="Markdown", reply_markup=None)
        else:
            await query.edit_message_text(text=text_msg, parse_mode="Markdown", reply_markup=None)
        db.close()
        return

    # Per skip e seen, mostriamo il prossimo film
    mood_str = context.user_data.get('selected_mood')
    if not mood_str:
        error_msg = "Oops! 🐮 Ho perso la memoria del tuo mood a causa di un riavvio di sistema.\nPer favore, usa di nuovo il comando /naviga per ricominciare!"
        if query.message.photo:
            await query.edit_message_caption(caption=error_msg, reply_markup=None)
        else:
            await query.edit_message_text(text=error_msg, reply_markup=None)
        db.close()
        return

    max_time = context.user_data.get('max_time', 999)
    min_time = context.user_data.get('min_time', 0)
    
    await render_movie_card(query, context, db, user, MoodType(mood_str), max_time, min_time)
    db.close()

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except BadRequest:
        pass
    
    # data is rate_{interaction_id}_{RATING}
    parts = query.data.split("_")
    interaction_id = int(parts[1])
    rating_str = parts[2]
    
    db = SessionLocal()
    interaction = db.query(UserInteraction).filter(UserInteraction.id == interaction_id).first()
    if interaction:
        interaction.rating = FeedbackRating(rating_str)
        
        # Check tier progression
        user = interaction.user
        seen_count = db.query(UserInteraction).filter(
            UserInteraction.user_id == user.id,
            UserInteraction.status.in_([InteractionStatus.SEEN, InteractionStatus.CHOSEN])
        ).count()
        
        if seen_count >= 5 and user.current_tier < 2:
            user.current_tier = 2
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="🎉 *Nuovo Pascolo Sbloccato! MOO!* 🐄\nHai ruminato abbastanza bagaglio culturale. Ora hai accesso ai film di Tier 2 (Deep Cuts)!",
                parse_mode="Markdown"
            )

        db.commit()
        
        response_text = {
            "REVELATORY": "Ottimo! Rinforzeremo questo pascolo per te. MOO!",
            "FORMATIVE": "Fantastico. Registrato nel tuo stomaco culturale. 🐄",
            "NOT_FOR_ME": "Moo... Ricevuto. Lo terremo a mente per evitare proposte simili."
        }
        
        await query.edit_message_text(
            text=f"Feedback registrato: {response_text.get(rating_str, 'Grazie!')}"
        )
    db.close()

def get_session_handlers():
    return [
        CallbackQueryHandler(handle_time_selection, pattern="^time_"),
        CallbackQueryHandler(handle_deck_action, pattern="^(skip|seen|choose)_"),
        CallbackQueryHandler(handle_feedback, pattern="^rate_")
    ]
