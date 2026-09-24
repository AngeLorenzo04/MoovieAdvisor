import asyncio
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from services.pipeline_service import run_pipeline_async, pipeline_state

async def popola_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Siccome questo bot e' privato, per ora permettiamo a chiunque di avviarlo.
    # Se vuoi puoi inserire un controllo su update.effective_user.id qui.
    
    if pipeline_state["is_running"]:
        await update.message.reply_text("⚠️ Il trattore è già in funzione! Bloccalo con /stop_popola prima di avviarlo di nuovo.")
        return
        
    limit = 10
    if context.args and context.args[0].isdigit():
        limit = int(context.args[0])
        
    # Avvia la pipeline in background come task asincrono
    asyncio.create_task(run_pipeline_async(limit, update.message.chat_id, context))
    await update.message.reply_text(f"🚜 OK! Avviato il download e l'analisi di {limit} film in background.\nTi avviserò se qualcosa va storto.")

async def stop_pipeline_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not pipeline_state["is_running"]:
        await query.edit_message_text(f"{query.message.text}\n\n*(Il trattore è già fermo!)*", parse_mode="Markdown")
        return
        
    pipeline_state["stop_requested"] = True
    await query.edit_message_text(f"{query.message.text}\n\n🛑 *Richiesta di blocco inviata. Il trattore si fermerà a breve.*", parse_mode="Markdown")

async def ultimi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database import SessionLocal
    from models import Movie
    db = SessionLocal()
    
    limit = 10
    if context.args and context.args[0].isdigit():
        limit = int(context.args[0])
        
    # Get latest added movies (highest IDs)
    recent = db.query(Movie).order_by(Movie.id.desc()).limit(limit).all()
    db.close()
    
    if not recent:
        await update.message.reply_text("Nessun film presente nel pascolo!")
        return
        
    msg = f"🎥 **Ultimi {len(recent)} film aggiunti:**\n\n"
    for m in recent:
        msg += f"• *{m.title}* ({m.year}) - Tier {m.min_tier_required} ({m.mood_tag.name})\n"
        
    await update.message.reply_text(msg, parse_mode="Markdown")

def get_admin_handlers():
    from telegram.ext import CallbackQueryHandler
    return [
        CommandHandler("popola", popola_cmd),
        CommandHandler("ultimi", ultimi_cmd),
        CallbackQueryHandler(stop_pipeline_callback, pattern="^stop_pipeline$")
    ]
