import os
import time
import json
import argparse
import requests
from google import genai
from dotenv import load_dotenv
from tqdm import tqdm

# Override print to work nicely with tqdm
print = tqdm.write

from database import SessionLocal
from models import Movie, MoodType

# Carica variabili d'ambiente
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Verifica chiavi
if not TMDB_API_KEY or TMDB_API_KEY == "il_tuo_tmdb_key_qui":
    print("ERRORE: Inserisci una TMDB_API_KEY valida in .env")
    exit(1)
if not GEMINI_API_KEY or GEMINI_API_KEY == "il_tuo_gemini_key_qui":
    print("ERRORE: Inserisci una GEMINI_API_KEY valida in .env")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_popular_movies(page=1):
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=it-IT&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Errore TMDb: {response.status_code}")
        return []

def fetch_movie_details(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=it-IT&append_to_response=credits"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def generate_curation_data(title, overview, director, year):
    prompt = f"""
Sei un esperto critico cinematografico. Analizza il film seguente:
Titolo: {title} ({year})
Regista: {director}
Trama: {overview}

Restituisci ESATTAMENTE e SOLO un oggetto JSON con questi campi:
- "mood_tag": scegli UNA tra queste 4 stringhe ESATTE: "DECOMPRESSION", "CATHARSIS", "HYPNOTIC", "INTROSPECTION".
- "movement_tag": (es. "Cyberpunk", "Neo-Noir", "Indie", etc. massimo 20 caratteri)
- "tier": (numero intero: 1 per capolavori famosi e imperdibili, 2 per film di nicchia, complessi o d'autore)
- "tech_innovation": (breve frase sull'innovazione tecnica o registica, max 150 caratteri)
- "cultural_legacy": (breve frase sull'impatto culturale, max 150 caratteri)
- "watch_tip": (un consiglio su cosa notare durante la visione, stile amichevole, max 150 caratteri)
"""
    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        text = response.text.strip()
        # Pulisci eventuali formattazioni markdown del JSON (es. ```json ... ```)
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        return json.loads(text.strip())
    except Exception as e:
        error_msg = str(e)
        print(f"Errore Generazione AI per {title}: {error_msg}")
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("Quota superata! Metto in pausa per 45 secondi...")
            time.sleep(45)
        elif "503" in error_msg or "UNAVAILABLE" in error_msg:
            print("Server sovraccarico! Metto in pausa per 10 secondi...")
            time.sleep(10)
        return None

def run_pipeline(limit=10):
    db = SessionLocal()
    added_count = 0
    page = 1
    
    print(f"🐮 Avvio pipeline TMDb + Gemini... Obiettivo: {limit} film.")
    
    pbar = tqdm(total=limit, desc="Popolamento Film", unit="film")
    
    while added_count < limit:
        print(f"\n--- Recupero pagina {page} da TMDb ---")
        movies = fetch_popular_movies(page)
        
        if not movies:
            break
            
        for tmdb_movie in movies:
            if added_count >= limit:
                break
                
            title = tmdb_movie.get('title')
            
            # Controlla se esiste già
            exists = db.query(Movie).filter(Movie.title == title).first()
            if exists:
                print(f"Skippato: {title} (già presente)")
                continue
                
            details = fetch_movie_details(tmdb_movie['id'])
            if not details:
                time.sleep(0.5)
                continue
                
            year = details.get('release_date', '0000')[:4]
            runtime = details.get('runtime', 0)
            poster_path = details.get('poster_path')
            overview = details.get('overview', '')
            
            # Trova il regista
            director = "Sconosciuto"
            if 'credits' in details and 'crew' in details['credits']:
                for crew_member in details['credits']['crew']:
                    if crew_member['job'] == 'Director':
                        director = crew_member['name']
                        break
            
            if not poster_path or not runtime or runtime == 0:
                continue # Salta film senza poster o durata
                
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            
            print(f"Analisi AI in corso per: {title} ({year})...")
            curation = generate_curation_data(title, overview, director, year)
            
            if not curation:
                time.sleep(3) # Anti rate-limit per l'API fallita
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
                pbar.update(1)
                print(f"✅ Aggiunto: {title} (Tier {new_movie.tier}, {new_movie.mood_tag.name})")
            except Exception as e:
                db.rollback()
                print(f"Errore DB per {title}: {e}")
            
            time.sleep(15) # Rispetta i rate limits di Gemini (15 RPM sul tier gratuito)
        
        page += 1
        
    db.close()
    pbar.close()
    print("\n🐄 Pipeline completata! MOO!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Popola il DB con TMDb e Gemini AI")
    parser.add_argument("--limit", type=int, default=10, help="Numero di film da aggiungere")
    args = parser.parse_args()
    
    run_pipeline(args.limit)
