# Cult MOOvie Advisor 🐄🎬

Cult MOOvie Advisor è un bot Telegram interattivo (e a tema bovino!) progettato per sconfiggere la "decision paralysis" serale. Invece di fungere da semplice motore di ricerca, il bot ti guida nella costruzione della tua cultura cinematografica tramite un'esperienza curata, percorsi tematici e un sistema a livelli (Tier), aiutato dall'Intelligenza Artificiale.

## ✨ Funzionalità Principali

- **Popolamento Intelligente (AI Pipeline):** Sfrutta l'API di TMDb per scaricare i film più popolari e usa l'intelligenza artificiale di Google Gemini per analizzarli, estrarre il "Mood" e assegnare automaticamente un Tier (1, 2 o 3) in base alla loro accessibilità cinematografica.
- **Deck di Carte (In-place UX):** Il bot non intasa la tua chat di Telegram. Ogni film suggerito viene mostrato come una "carta" con locandina, sinossi e pillole critiche. Tramite pulsanti inline puoi saltarlo, segnarlo come già visto, o sceglierlo, aggiornando sempre lo stesso messaggio.
- **Filtri Situazionali:** Inserisci il tuo mood (Decompressione, Catarsi, Ipnotico, Introspezione) e il tempo a tua disposizione per ricevere un consiglio mirato.
- **Skill Tree & Gamification (`/skills`):** Parti dal "Tier 1" (I Pilastri). Più film guardi e valuti, più la tua barra dell'esperienza sale, sbloccando film sempre più autoriali e complessi nei livelli successivi.

## 🛠️ Stack Tecnologico

- **Linguaggio:** Python 3.11+
- **Framework Telegram:** `python-telegram-bot` (v20+ async)
- **Database & ORM:** SQLite + SQLAlchemy 2.0
- **AI & Data Pipelines:** Google Gemini API (`google-genai`) + TMDb API
- **Scheduling:** JobQueue integrata per feedback asincroni.

## 🚀 Guida all'installazione

### 1. Requisiti e Ambiente Virtuale
Clona il progetto e crea un ambiente virtuale (consigliato `conda`):
```bash
conda create -n film python=3.11 -y
conda activate film
pip install -r requirements.txt
```

### 2. Configurare le variabili d'ambiente
Apri il file `.env` (crealo se non esiste) e inserisci le tue chiavi API segrete:
```env
TELEGRAM_BOT_TOKEN=token_di_botfather
TMDB_API_KEY=tua_chiave_tmdb
GEMINI_API_KEY=tua_chiave_google_gemini
DB_URL=sqlite:///db.sqlite3
```

### 3. Popolare il Database con l'Intelligenza Artificiale
Il catalogo si riempie in automatico analizzando i film con Gemini. Per scaricare e analizzare i film, avvia la pipeline:
```bash
# Scarica ad esempio i primi 1000 film più popolari
python tmdb_pipeline.py --limit 1000
```
*(Nota: L'operazione può richiedere un po' di tempo a causa dei rate limit dell'API gratuita di Gemini. Lo script gestirà in automatico pause e sovraccarichi di rete).*

### 4. Avviare il bot
```bash
python bot.py
```
Ora apri Telegram, cerca il tuo bot e premi `/start`!

## 🎮 Comandi del Bot

- `/start`: Messaggio di benvenuto e iniziazione alla setta bovina.
- `/naviga`: Avvia il flusso di ricerca (quiz per Mood e durata).
- `/skills` (o `/profilo`): Mostra le tue statistiche, i film visti e i progressi per salire di Tier!
