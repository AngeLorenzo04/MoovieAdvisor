# Cult MOOvie Advisor 🐄🎬

Cult MOOvie Advisor è un bot Telegram interattivo (e a tema bovino!) progettato per sconfiggere la "decision paralysis" serale. Invece di fungere da semplice motore di ricerca, il bot ti guida nella costruzione della tua cultura cinematografica tramite un'esperienza curata, percorsi tematici e un sistema a livelli (Tier).

## ✨ Funzionalità Principali

- **Deck di Carte (In-place UX):** Il bot non intasa la tua chat di Telegram. Ogni film suggerito viene mostrato come una "carta" con locandina, sinossi e pillole critiche. Tramite pulsanti inline puoi saltarlo, segnarlo come già visto, o sceglierlo, aggiornando sempre lo stesso messaggio.
- **Filtri Situazionali:** Inserisci il tuo mood (Decompressione, Catarsi, Ipnotico, Introspezione) e il tempo a tua disposizione per ricevere un consiglio mirato.
- **Skill Tree & Gamification (`/skills`):** Parti dal "Tier 1" (I Pilastri). Più film guardi e valuti, più la tua barra dell'esperienza sale. Sbloccando il "Tier 2", avrai accesso a capolavori cinematografici più complessi e sotterranei ("Deep Cuts").
- **Loop di Feedback Asincrono:** Dopo aver scelto un film, il bot ti contatterà più tardi in automatico per chiederti che impatto ha avuto su di te (es. Rivelatorio, Formativo), registrando l'informazione nel tuo bagaglio culturale.

## 🛠️ Stack Tecnologico

- **Linguaggio:** Python 3.11+
- **Framework Telegram:** `python-telegram-bot` (v20+ async)
- **Database & ORM:** SQLite + SQLAlchemy 2.0
- **Scheduling:** JobQueue integrata per messaggi ritardati.

## 🚀 Guida all'installazione

### 1. Clonare/Scaricare la repository
Assicurati di essere nella cartella del progetto:
```bash
cd Film_Advisor
```

### 2. Creare l'ambiente virtuale
È consigliato usare `conda` o `venv`. Con Conda:
```bash
conda create -n film python=3.11 -y
conda activate film
```

### 3. Installare le dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configurare le variabili d'ambiente
Apri il file `.env` (crealo se non esiste) e inserisci il token fornito da [@BotFather](https://t.me/BotFather) su Telegram:
```env
TELEGRAM_BOT_TOKEN=il_tuo_token_qui
DB_URL=sqlite:///db.sqlite3
```

### 5. Popolare il Database (Seed)
Prima di avviare il bot, è necessario caricare il catalogo iniziale dei film nel database SQLite:
```bash
python seed.py
```
*(Opzionale: puoi aggiungere ulteriori film curati eseguendo `python add_more_movies.py`)*

### 6. Avviare il bot
```bash
python bot.py
```
Ora apri Telegram, cerca il nome del tuo bot e premi `/start`!

## 🎮 Comandi del Bot

- `/start`: Messaggio di benvenuto e spiegazione del funzionamento.
- `/naviga`: Avvia il flusso di ricerca chiedendoti il mood e il tempo a disposizione.
- `/skills` (o `/profilo`): Mostra le tue statistiche, i film visti e i progressi verso il prossimo livello (Tier).
