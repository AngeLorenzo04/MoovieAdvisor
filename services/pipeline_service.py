import os
import asyncio
import json
import httpx
from google import genai
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import SessionLocal
from models import Movie, MoodType

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-1.5-flash")

pipeline_state = {
    "is_running": False,
    "stop_requested": False
}

async def fetch_popular_movies_async(page=1):
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=it-IT&page={page}"
    async with httpx.AsyncClient() as c:
        response = await c.get(url)
        if response.status_code == 200:
            return response.json().get('results', [])
    return []

async def fetch_movie_details_async(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=it-IT&append_to_response=credits"
    async with httpx.AsyncClient() as c:
        response = await c.get(url)
        if response.status_code == 200:
            return response.json()
    return None

async def generate_curation_data_async(title, overview, director, year):
    prompt = f"""
Sei un critico cinematografico. Analizza il film:
Titolo: {title} ({year})
Regista: {director}
Trama: {overview}

Restituisci ESATTAMENTE e SOLO un oggetto JSON con questi campi:
- "mood_tag": scegli UNA tra queste 4 stringhe ESATTE: "DECOMPRESSION", "CATHARSIS", "HYPNOTIC", "INTROSPECTION".
- "movement_tag": (es. "Cyberpunk", "Neo-Noir", "Indie", ecc. max 20 caratteri)
- "tier": (intero: 1 per film famosi, 2 per nicchia o d'autore, 3 per film complessi)
- "tech_innovation": (breve frase, max 150 caratteri)
- "cultural_legacy": (breve frase, max 150 caratteri)
- "watch_tip": (un consiglio su cosa notare durante la visione, max 150 caratteri)
"""
    try:
        if OPENROUTER_API_KEY:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }
            async with httpx.AsyncClient() as c:
                response = await c.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=60.0)
                result = response.json()
                if "error" in result:
                    return str(result["error"])
                text = result["choices"][0]["message"]["content"].strip()
        else:
            response = await client.aio.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            text = response.text.strip()
            
        if text.startswith("```json"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        return str(e)

async def run_pipeline_async(limit, chat_id, context):
    pipeline_state["is_running"] = True
    pipeline_state["stop_requested"] = False
    
    db = SessionLocal()
    added_count = 0
    page = 1
    
    keyboard = [[InlineKeyboardButton("🛑 Ferma il Trattore", callback_data="stop_pipeline")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=f"🚜 Avvio del trattore per raccogliere {limit} film...", reply_markup=reply_markup)
    
    try:
        while added_count < limit:
            if pipeline_state["stop_requested"]:
                await context.bot.send_message(chat_id=chat_id, text="🛑 Pipeline bloccata manualmente! Il trattore si è fermato.")
                break
                
            movies = await fetch_popular_movies_async(page)
            if not movies:
                break
                
            for tmdb_movie in movies:
                if added_count >= limit or pipeline_state["stop_requested"]:
                    break
                    
                title = tmdb_movie.get('title')
                exists = db.query(Movie).filter(Movie.title == title).first()
                if exists:
                    continue
                    
                details = await fetch_movie_details_async(tmdb_movie['id'])
                if not details:
                    await asyncio.sleep(0.5)
                    continue
                    
                year = details.get('release_date', '0000')[:4]
                runtime = details.get('runtime', 0)
                poster_path = details.get('poster_path')
                overview = details.get('overview', '')
                
                director = "Sconosciuto"
                if 'credits' in details and 'crew' in details['credits']:
                    for crew_member in details['credits']['crew']:
                        if crew_member['job'] == 'Director':
                            director = crew_member['name']
                            break
                
                if not poster_path or not runtime or runtime == 0:
                    continue
                    
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                
                curation = await generate_curation_data_async(title, overview, director, year)
                
                if isinstance(curation, str): # Error message
                    error_msg = curation
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Limite API raggiunto su {title}. Pausa 45s per raffreddare i motori...")
                        await asyncio.sleep(45)
                    elif "503" in error_msg or "UNAVAILABLE" in error_msg:
                        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Server Google sovraccarico (Errore 503) su {title}. Pausa di 15 secondi... 😴")
                        await asyncio.sleep(15)
                    else:
                        keyboard = [[InlineKeyboardButton("🛑 Ferma il Trattore", callback_data="stop_pipeline")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Errore Intelligenza Artificiale per *{title}*:\n{error_msg}", parse_mode="Markdown", reply_markup=reply_markup)
                        await asyncio.sleep(3)
                    continue
                    
                try:
                    mood_enum = MoodType[curation['mood_tag']]
                    new_movie = Movie(
                        title=title,
                        year=int(year) if year.isdigit() else 0,
                        runtime=runtime,
                        director=director,
                        poster_url=poster_url,
                        mood_tag=mood_enum,
                        movement_tag=curation.get('movement_tag', 'Classico'),
                        tier=curation.get('tier', 1),
                        tech_innovation=curation.get('tech_innovation', 'N/A'),
                        cultural_legacy=curation.get('cultural_legacy', 'N/A'),
                        watch_tip=curation.get('watch_tip', 'Buona visione!')
                    )
                    db.add(new_movie)
                    db.commit()
                    added_count += 1
                    
                    # Notifica ogni 10 film per far sapere che è vivo
                    if added_count % 10 == 0:
                        keyboard = [[InlineKeyboardButton("🛑 Ferma il Trattore", callback_data="stop_pipeline")]]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await context.bot.send_message(chat_id=chat_id, text=f"📊 Aggiornamento: Aggiunti {added_count}/{limit} film.", reply_markup=reply_markup)
                        
                except Exception as e:
                    db.rollback()
                    keyboard = [[InlineKeyboardButton("🛑 Ferma il Trattore", callback_data="stop_pipeline")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await context.bot.send_message(chat_id=chat_id, text=f"❌ Errore Database per *{title}*: {e}", parse_mode="Markdown", reply_markup=reply_markup)
                
                await asyncio.sleep(15) # Rispetta il Rate Limit
                
            page += 1
            
        if not pipeline_state["stop_requested"]:
            await context.bot.send_message(chat_id=chat_id, text=f"✅ Lavoro completato! Il trattore ha scaricato {added_count} nuovi film nel database. MOO! 🐄")
            
    except Exception as e:
        keyboard = [[InlineKeyboardButton("🛑 Ferma il Trattore", callback_data="stop_pipeline")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text=f"🔥 ERRORE FATALE NELLA PIPELINE:\n{e}", reply_markup=reply_markup)
    finally:
        db.close()
        pipeline_state["is_running"] = False

