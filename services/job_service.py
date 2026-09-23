from telegram.ext import ContextTypes
from database import SessionLocal
from models import UserInteraction

async def check_in_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Scheduled job that sends a message to the user asking for feedback
    on a movie they chose.
    """
    job = context.job
    chat_id = job.chat_id
    movie_title = job.data.get('movie_title')
    interaction_id = job.data.get('interaction_id')
    
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = [
        [InlineKeyboardButton("🤯 Rivelatorio", callback_data=f"rate_{interaction_id}_REVELATORY")],
        [InlineKeyboardButton("🧠 Formativo", callback_data=f"rate_{interaction_id}_FORMATIVE")],
        [InlineKeyboardButton("🥱 Non nelle mie corde", callback_data=f"rate_{interaction_id}_NOT_FOR_ME")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"🐮 Hai finito di ruminare *{movie_title}*.\n\nChe impatto ha avuto sul tuo stomaco? MOO!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def schedule_post_viewing_check(context: ContextTypes.DEFAULT_TYPE, chat_id: int, movie_title: str, runtime: int, interaction_id: int):
    """
    Schedules the check-in job. 
    Formula: runtime (minutes) + buffer (e.g. 10 mins).
    For testing purposes, we'll override this to just 10 seconds if runtime < 0 (not used yet, but good for debug).
    """
    # For a real scenario: delay = (runtime + 10) * 60
    # For easier local testing: wait 10 seconds
    delay_seconds = 10 
    
    context.job_queue.run_once(
        check_in_job, 
        when=delay_seconds, 
        chat_id=chat_id, 
        data={'movie_title': movie_title, 'interaction_id': interaction_id},
        name=f"checkin_{interaction_id}"
    )
