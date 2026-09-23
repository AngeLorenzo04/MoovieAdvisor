from database import init_db, SessionLocal
from models import Movie, MoodType

def seed_movies():
    db = SessionLocal()
    
    # Check if we already have movies
    if db.query(Movie).count() > 0:
        print("Database already seeded.")
        db.close()
        return

    movies = [
        # DECOMPRESSION
        Movie(
            title="The Big Lebowski",
            year=1998,
            runtime=117,
            director="Joel Coen, Ethan Coen",
            poster_url="https://image.tmdb.org/t/p/w500/rr95tUUDf2iG538S0RzKntG7QzL.jpg",
            mood_tag=MoodType.DECOMPRESSION,
            movement_tag="Postmodern Noir",
            tier=1,
            tech_innovation="Uso virtuosistico dei dream sequences (sequenze oniriche) coreografati a tempo di musica.",
            cultural_legacy="Ha generato una vera e propria religione ('Dudeism') e ridefinito la commedia surreale degli anni '90.",
            watch_tip="Fai attenzione a come il Drugo risolve (o non risolve) la trama: il film decostruisce le classiche regole del giallo."
        ),
        Movie(
            title="Amélie (Le Fabuleux Destin d'Amélie Poulain)",
            year=2001,
            runtime=122,
            director="Jean-Pierre Jeunet",
            poster_url="https://image.tmdb.org/t/p/w500/mX3WzvNDhhfcjxsDkEU78YVqRHz.jpg",
            mood_tag=MoodType.DECOMPRESSION,
            movement_tag="Realismo Magico",
            tier=1,
            tech_innovation="Uso estremo della color grading digitale (dominanti verde, rosso e giallo) per creare un mondo fiabesco.",
            cultural_legacy="Ha influenzato l'estetica indie e del 'quirky' cinema europeo per oltre un decennio.",
            watch_tip="Nota come la macchina da presa si muove fluidamente (spesso in soggettiva) per trasmettere il punto di vista infantile e curioso della protagonista."
        ),
        # CATHARSIS
        Movie(
            title="Pulp Fiction",
            year=1994,
            runtime=154,
            director="Quentin Tarantino",
            poster_url="https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPbOYKQmi51.jpg",
            mood_tag=MoodType.CATHARSIS,
            movement_tag="New Hollywood / Pulp",
            tier=1,
            tech_innovation="Narrazione non lineare perfetta: intreccia tre storie in modo circolare senza confondere lo spettatore.",
            cultural_legacy="Ha riscritto le regole del dialogo cinematografico (la pop-culture come elemento drammatico) e generato infiniti cloni.",
            watch_tip="Ascolta attentamente i dialoghi apparentemente futili: servono a umanizzare criminali spietati prima dell'azione esplosiva."
        ),
        Movie(
            title="Mad Max: Fury Road",
            year=2015,
            runtime=120,
            director="George Miller",
            poster_url="https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg",
            mood_tag=MoodType.CATHARSIS,
            movement_tag="Action Post-Apocalittico",
            tier=1,
            tech_innovation="Montaggio 'center-framed': l'azione principale è sempre al centro dello schermo, rendendo leggibile un ritmo forsennato.",
            cultural_legacy="Ha dimostrato che il cinema action può essere pura poesia visiva e arte autoriale ad alto budget.",
            watch_tip="Osserva come i personaggi comunicano quasi esclusivamente tramite sguardi e gesti; i dialoghi sono ridotti all'osso."
        ),
        # HYPNOTIC
        Movie(
            title="Blade Runner",
            year=1982,
            runtime=117,
            director="Ridley Scott",
            poster_url="https://image.tmdb.org/t/p/w500/63N9q8C6KxDb1eF8c4149yB9MKE.jpg",
            mood_tag=MoodType.HYPNOTIC,
            movement_tag="Cyberpunk",
            tier=1,
            tech_innovation="Integrazione pionieristica di effetti speciali pratici, matte painting e luci al neon, creando un'estetica invecchiata magistralmente.",
            cultural_legacy="Ha codificato visivamente l'intero genere Cyberpunk. Quasi ogni film sci-fi successivo ne porta i segni.",
            watch_tip="Fai caso al tema degli occhi (inquadrature, riflessi, gufi finti) come metafora dell'anima e della memoria."
        ),
        Movie(
            title="Stalker",
            year=1979,
            runtime=162,
            director="Andrei Tarkovsky",
            poster_url="https://image.tmdb.org/t/p/w500/xV1G6eC2F2i68hP8Lq4c1lVqf2u.jpg",
            mood_tag=MoodType.HYPNOTIC,
            movement_tag="Sci-Fi Filosofico / Cinema Sovietico",
            tier=2,
            tech_innovation="Uso magistrale di piani sequenza lentissimi (long takes) per alterare la percezione del tempo nello spettatore.",
            cultural_legacy="Caposaldo del cinema meditativo; ha ispirato videogiochi e una vasta gamma di cinema autoriale.",
            watch_tip="Nota il passaggio dalla monocromia (seppia) del mondo reale ai colori quando entrano nella misteriosa 'Zona'."
        ),
        # INTROSPECTION
        Movie(
            title="Taxi Driver",
            year=1976,
            runtime=114,
            director="Martin Scorsese",
            poster_url="https://image.tmdb.org/t/p/w500/ekstpH614fwDX8DUln1a2Opz0N8.jpg",
            mood_tag=MoodType.INTROSPECTION,
            movement_tag="New Hollywood",
            tier=1,
            tech_innovation="Uso dell'illuminazione espressionista e slow-motion per visualizzare il degrado mentale e urbano (New York come inferno).",
            cultural_legacy="Ha definito l'archetipo dell'antieroe moderno e alienato. Una pietra miliare dell'indagine psicologica su schermo.",
            watch_tip="Fai attenzione a come la colonna sonora di Bernard Herrmann enfatizzi il senso di solitudine e paranoia di Travis."
        ),
        Movie(
            title="Persona",
            year=1966,
            runtime=83,
            director="Ingmar Bergman",
            poster_url="https://image.tmdb.org/t/p/w500/5gVdO1b74LidB04hB4K5W7F1Ue8.jpg",
            mood_tag=MoodType.INTROSPECTION,
            movement_tag="Cinema Modernista",
            tier=2,
            tech_innovation="Decostruzione del mezzo cinematografico stesso: la pellicola si brucia e si rompe letteralmente durante il film.",
            cultural_legacy="L'opera massima sull'identità e la doppiezza umana; innumerevoli registi vi fanno riferimento visivo (i volti sovrapposti).",
            watch_tip="Cerca di isolare il confine tra le due protagoniste: Bergman usa luci e composizioni per fonderle in una sola identità."
        )
    ]

    db.add_all(movies)
    db.commit()
    print(f"Seeded {len(movies)} movies successfully.")
    db.close()

if __name__ == "__main__":
    init_db()
    seed_movies()
