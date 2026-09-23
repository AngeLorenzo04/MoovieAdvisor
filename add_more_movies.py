from database import SessionLocal
from models import Movie, MoodType

def add_more_movies():
    db = SessionLocal()
    
    new_movies = [
        # DECOMPRESSION
        Movie(
            title="The Grand Budapest Hotel", year=2014, runtime=99, director="Wes Anderson",
            poster_url="https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg",
            mood_tag=MoodType.DECOMPRESSION, movement_tag="Quirky Indie", tier=1,
            tech_innovation="Uso maniacale della simmetria centrale e formati d'aspetto mutevoli (aspect ratio) per riflettere le diverse epoche.",
            cultural_legacy="Ha consacrato l'estetica 'pastel-goth' e perfezionato il diorama cinematografico moderno.",
            watch_tip="Fai caso a come ogni inquadratura sembri un quadro perfettamente bilanciato."
        ),
        Movie(
            title="Little Miss Sunshine", year=2006, runtime=101, director="Jonathan Dayton, Valerie Faris",
            poster_url="https://image.tmdb.org/t/p/w500/wufzZk4KjB9C9E1jJk7wI60oJ82.jpg",
            mood_tag=MoodType.DECOMPRESSION, movement_tag="Indie Road Movie", tier=1,
            tech_innovation="Ridefinizione della commedia corale indipendente, bilanciando umorismo nero e vulnerabilità emotiva.",
            cultural_legacy="Ha lanciato il trend dei 'Sundance Darlings', film indipendenti dal grande cuore e dal piccolo budget.",
            watch_tip="Osserva come il furgoncino giallo diventi un microcosmo che forza i personaggi a risolvere i loro conflitti."
        ),
        Movie(
            title="Singin' in the Rain", year=1952, runtime=103, director="Stanley Donen, Gene Kelly",
            poster_url="https://image.tmdb.org/t/p/w500/4gOqU5t8q2pG55Y9L0xYm8m3X2.jpg",
            mood_tag=MoodType.DECOMPRESSION, movement_tag="Musical Classico", tier=2,
            tech_innovation="Integrazione perfetta e fluida tra numeri musicali e progressione narrativa (prima spesso scollegati).",
            cultural_legacy="Spesso considerato il più grande musical della storia, una lettera d'amore (e satira) a Hollywood.",
            watch_tip="Guarda la coreografia della title track: Kelly era malato e aveva la febbre a 39, eppure i movimenti sono di una leggerezza inaudita."
        ),
        
        # CATHARSIS
        Movie(
            title="The Matrix", year=1999, runtime=136, director="The Wachowskis",
            poster_url="https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            mood_tag=MoodType.CATHARSIS, movement_tag="Cyberpunk / Action", tier=1,
            tech_innovation="Invenzione del 'Bullet Time', una tecnica di ripresa con decine di macchine fotografiche interpolate digitalmente.",
            cultural_legacy="Ha unito la filosofia cyberpunk, gli anime e il kung fu di Hong Kong nel blockbuster definitivo degli anni '90.",
            watch_tip="Nota il colore verde (stile vecchi monitor a fosfori) che domina ogni scena ambientata dentro Matrix."
        ),
        Movie(
            title="Oldboy", year=2003, runtime=120, director="Park Chan-wook",
            poster_url="https://image.tmdb.org/t/p/w500/pWDtjs568ZfOTMbURQBYuT4Qxka.jpg",
            mood_tag=MoodType.CATHARSIS, movement_tag="New Korean Cinema", tier=2,
            tech_innovation="Uso magistrale del piano sequenza laterale (la famosa scena del corridoio) per trasmettere puro sfinimento e violenza realistica.",
            cultural_legacy="Ha portato il cinema sudcoreano estremo all'attenzione globale, influenzando Tarantino e tutto l'action moderno.",
            watch_tip="Durante la rissa nel corridoio, conta quanto tempo passa senza alcuno stacco di montaggio."
        ),
        Movie(
            title="Kill Bill: Vol. 1", year=2003, runtime=111, director="Quentin Tarantino",
            poster_url="https://image.tmdb.org/t/p/w500/v7TaX8kXMXs5yFFGR41guUDNcnB.jpg",
            mood_tag=MoodType.CATHARSIS, movement_tag="Pulp / Arti Marziali", tier=1,
            tech_innovation="Pastiche estremo: cambia formati, stili visivi e persino mezzi (animazione anime inserita nel live action) fluidamente.",
            cultural_legacy="Un monumento alla vendetta femminile e una dichiarazione d'amore esplosiva al cinema d'exploitation.",
            watch_tip="Ascolta l'uso meticoloso degli effetti sonori e della musica come elemento ritmico per le spade."
        ),
        
        # HYPNOTIC
        Movie(
            title="2001: A Space Odyssey", year=1968, runtime=149, director="Stanley Kubrick",
            poster_url="https://image.tmdb.org/t/p/w500/mMtUyw1EdrV65b0O1fQ9pBv07G.jpg",
            mood_tag=MoodType.HYPNOTIC, movement_tag="Sci-Fi Epico", tier=1,
            tech_innovation="Effetti speciali ottici pazzeschi realizzati a mano anni prima del digitale e uso sublime del 'match cut' ellittico.",
            cultural_legacy="Ha elevato la fantascienza a genere filosofico 'serio'. Senza questo, non avremmo avuto Star Wars o Interstellar.",
            watch_tip="Osserva come l'intelligenza artificiale HAL 9000 esprima emozioni umane meglio degli attori veri."
        ),
        Movie(
            title="Spirited Away (La Città Incantata)", year=2001, runtime=125, director="Hayao Miyazaki",
            poster_url="https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkBgkAB.jpg",
            mood_tag=MoodType.HYPNOTIC, movement_tag="Anime / Fantasy", tier=1,
            tech_innovation="Il concetto di 'Ma' (vuoto/pausa): inquadrature silenziose inserite per far riposare l'occhio e riflettere.",
            cultural_legacy="L'anime di maggior successo globale, ha sdoganato l'animazione d'autore giapponese all'estero vincendo l'Oscar.",
            watch_tip="La scena del viaggio in treno sull'acqua: un capolavoro di silenzio e riflessione."
        ),
        Movie(
            title="Mulholland Drive", year=2001, runtime=147, director="David Lynch",
            poster_url="https://image.tmdb.org/t/p/w500/oVQO3ySOW55S1yGzL2YqRk8t8.jpg",
            mood_tag=MoodType.HYPNOTIC, movement_tag="Surrealismo Moderno", tier=2,
            tech_innovation="Costruzione onirica fratturata in cui l'inconscio dei personaggi modella fisicamente la realtà filmica.",
            cultural_legacy="Definito da molti critici come il miglior film del XXI secolo, la decostruzione definitiva di Hollywood.",
            watch_tip="Cerca di non dare senso logico a tutto subito, ma lasciati guidare dalla logica del 'sogno'."
        ),

        # INTROSPECTION
        Movie(
            title="8½ (Otto e mezzo)", year=1963, runtime=138, director="Federico Fellini",
            poster_url="https://image.tmdb.org/t/p/w500/1XwYyUqXyF5B2Fz7B9Z9Z5r9G2.jpg",
            mood_tag=MoodType.INTROSPECTION, movement_tag="Neorealismo Magico / Cinema d'Autore", tier=2,
            tech_innovation="Il 'flusso di coscienza' visivo: sogni, ricordi e realtà si fondono senza stacchi evidenti.",
            cultural_legacy="Il film definitivo sul blocco creativo e sulla crisi d'ispirazione. Omaggialo, copiato, venerato.",
            watch_tip="La celebre scena iniziale dell'ingorgo nel traffico: puro incubo felliniano, in silenzio surreale."
        ),
        Movie(
            title="Eternal Sunshine of the Spotless Mind", year=2004, runtime=108, director="Michel Gondry",
            poster_url="https://image.tmdb.org/t/p/w500/5MwkWH9tx75GweNJpOyPE0lZ.jpg",
            mood_tag=MoodType.INTROSPECTION, movement_tag="Indie Sci-Fi Romance", tier=1,
            tech_innovation="Effetti speciali visivi 'in camera' (fatti dal vivo senza CGI) per rappresentare la memoria che crolla.",
            cultural_legacy="Ha distrutto i cliché del film romantico, affrontando in modo adulto il dolore e l'accettazione.",
            watch_tip="Ogni volta che l'ambiente svanisce o diventa incoerente (es. i libri senza titoli), è una memoria che viene cancellata in tempo reale."
        ),
        Movie(
            title="Her (Lei)", year=2013, runtime=126, director="Spike Jonze",
            poster_url="https://image.tmdb.org/t/p/w500/aHq6iBIV2vBivtYxT4f16b.jpg",
            mood_tag=MoodType.INTROSPECTION, movement_tag="Sci-Fi Esistenziale", tier=1,
            tech_innovation="Fotografia che usa colori pastello e caldi (contrari alla solita sci-fi fredda e blu) per una distopia molto 'accogliente'.",
            cultural_legacy="Un'esplorazione incredibilmente preveggente della solitudine digitale e dei rapporti parasociali con le AI.",
            watch_tip="Osserva i colori dei vestiti di Theodore (Joaquin Phoenix) e come si evolvono in base al suo stato emotivo con l'IA Samantha."
        )
    ]

    added = 0
    for m in new_movies:
        # Check se esiste già
        exists = db.query(Movie).filter(Movie.title == m.title).first()
        if not exists:
            db.add(m)
            added += 1

    db.commit()
    print(f"MOO! Aggiunti {added} nuovi film alla stalla!")
    db.close()

if __name__ == "__main__":
    add_more_movies()
