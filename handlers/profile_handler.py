from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import SessionLocal
from services.movie_service import get_or_create_user, get_user_stats

async def skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    user = get_or_create_user(db, update.effective_user.id)
    stats = get_user_stats(db, user)
    db.close()
    
    tier_name = "I Pilastri" if stats['current_tier'] == 1 else "Deep Cuts"
    
    # Create a progress bar
    progress_bar_length = 10
    filled_blocks = int((stats['tier_progress'] / 100) * progress_bar_length)
    empty_blocks = progress_bar_length - filled_blocks
    progress_bar = "█" * filled_blocks + "░" * empty_blocks
    
    message = (
        f"🐄 *Il tuo Profilo Bovino (Cinefilo)* 🐄\n\n"
        f"🎬 *Film ruminati:* {stats['total_seen']}\n"
        f"🎖 *Livello Corrente:* Tier {stats['current_tier']} ({tier_name})\n\n"
        f"Progressione verso il prossimo Pascolo:\n"
        f"[{progress_bar}] {stats['tier_progress']}%\n"
    )
    
    if stats['current_tier'] < 3:
         missing = max(0, stats['movies_needed_for_next_tier'] - stats['streak_seen'])
         message += f"\nBruca altri {missing} film per sbloccare il Tier {stats['current_tier'] + 1}! MOO!"
    else:
         message += f"\nHai raggiunto il livello massimo! Il Grande Bovino è fiero di te! MUUU! 🐮"

    await update.message.reply_text(message, parse_mode="Markdown")

def get_profile_handlers():
    return [
        CommandHandler("skills", skills),
        CommandHandler("profilo", skills)
    ]
