import os
import asyncio
import httpx
from dotenv import load_dotenv
from database import SessionLocal
from models import Movie, MoodType

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def assign_curation(genres, year):
    # Mapping logico basato sui generi TMDB
    mood = MoodType.DECOMPRESSION
    tier = 1
    movement = "Cinema Contemporaneo"
    
    if year < 1970:
        movement = "Epoca d'Oro di Hollywood"
        tier = 3
    elif year < 1990:
        movement = "Nuova Hollywood / Blockbuster Era"
        tier = 2
        
    if 18 in genres: # Drama
        mood = MoodType.INTROSPECTION
        tier = max(tier, 2)
    if 27 in genres or 53 in genres: # Horror / Thriller
        mood = MoodType.CATHARSIS
        tier = max(tier, 2)
    if 878 in genres or 14 in genres: # Sci-Fi / Fantasy
        mood = MoodType.HYPNOTIC
    if 35 in genres or 16 in genres: # Comedy / Animation
        mood = MoodType.DECOMPRESSION
        tier = 1
        
    return {
        "mood_tag": mood,
        "tier": tier,
        "movement_tag": movement,
        "tech_innovation": "Notevole uso di fotografia e montaggio per l'epoca." if year < 2000 else "Standard produttivi moderni di altissima qualità.",
        "cultural_legacy": "Un caposaldo del suo genere, citato innumerevoli volte nella cultura pop.",
        "watch_tip": "Spegnere il cellulare. Richiede attenzione ma ripaga con forti emozioni." if tier >= 2 else "Perfetto per una serata relax con popcorn."
    }

async def fetch_movie_details(client, movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=it-IT&append_to_response=credits"
    try:
        r = await client.get(url, timeout=10.0)
        return r.json()
    except:
        return None

async def seed():
    print("🚜 Inizio Iniezione di Massa: Recupero i 40 film più votati della storia...")
    db = SessionLocal()
    added = 0
    
    async with httpx.AsyncClient() as client:
        # Recupera 25 pagine (20 film per pagina = 500 film)
        for page in range(1, 26):
            print(f"📄 Scraping Pagina {page}/25 da TMDB...")
            url = f"{TMDB_BASE_URL}/movie/top_rated?api_key={TMDB_API_KEY}&language=it-IT&page={page}"
            r = await client.get(url)
            movies = r.json().get('results', [])
            
            for tmdb_m in movies:
                title = tmdb_m.get('title')
                
                if db.query(Movie).filter(Movie.title == title).first():
                    print(f"⏭️ Già presente: {title}")
                    continue
                    
                details = await fetch_movie_details(client, tmdb_m['id'])
                if not details:
                    continue
                    
                year = int(details.get('release_date', '0000')[:4]) if details.get('release_date') else 0
                runtime = details.get('runtime', 0)
                poster_path = details.get('poster_path')
                overview = details.get('overview', '')
                
                if not poster_path or not runtime:
                    continue
                    
                director = "Sconosciuto"
                if 'credits' in details and 'crew' in details['credits']:
                    for c in details['credits']['crew']:
                        if c['job'] == 'Director':
                            director = c['name']
                            break
                            
                genres = [g['id'] for g in details.get('genres', [])]
                curation = assign_curation(genres, year)
                
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                
                new_movie = Movie(
                    title=title,
                    year=year,
                    runtime=runtime,
                    director=director,
                    poster_url=poster_url,
                    mood_tag=curation['mood_tag'],
                    movement_tag=curation['movement_tag'],
                    tier=curation['tier'],
                    tech_innovation=curation['tech_innovation'],
                    cultural_legacy=curation['cultural_legacy'],
                    watch_tip=curation['watch_tip']
                )
                db.add(new_movie)
                added += 1
                print(f"✅ Inserito: {title} (Tier {curation['tier']}, {curation['mood_tag'].value})")
                
    db.commit()
    db.close()
    print(f"\n🎉 Iniezione completata! Aggiunti {added} capolavori al pascolo.")

if __name__ == "__main__":
    asyncio.run(seed())
