import sqlite3
import sys

def get_tables(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return [row[0] for row in c.fetchall()]

def get_columns(c, table):
    c.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in c.fetchall()]

def draw_dynamic_table(columns, rows):
    if not rows:
        print("\n❌ Nessun record trovato con questi filtri.")
        return

    # Calcola la larghezza massima per ogni colonna
    col_widths = [len(col) for col in columns]
    for row in rows:
        for i, val in enumerate(row):
            val_str = str(val).replace('\n', ' ')
            # Troncamento se troppo lungo per evitare che esploda lo schermo
            if len(val_str) > 40:
                val_str = val_str[:37] + "..."
            col_widths[i] = max(col_widths[i], len(val_str))
            
    # Crea la riga superiore
    top = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    # Crea l'intestazione
    header = "│" + "│".join(f" {col.center(w)} " for col, w in zip(columns, col_widths)) + "│"
    # Crea il separatore
    sep = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    # Crea il fondo
    bottom = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
    
    print("\n" + top)
    print(header)
    print(sep)
    
    for row in rows:
        row_str = "│"
        for i, val in enumerate(row):
            val_str = str(val).replace('\n', ' ')
            if len(val_str) > 40:
                val_str = val_str[:37] + "..."
            row_str += f" {val_str.ljust(col_widths[i])} │"
        print(row_str)
        
    print(bottom)
    print(f"📊 Totale record mostrati: {len(rows)}\n")

def main():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    
    tables = get_tables(c)
    if not tables:
        print("Il database è vuoto!")
        return
        
    print("🐄 BENVENUTO NEL MOO-DB VIEWER 🐄")
    print("Tabelle disponibili:")
    for i, t in enumerate(tables, 1):
        print(f" {i}. {t}")
        
    t_idx = input(f"\nScegli il numero della tabella (1-{len(tables)}): ").strip()
    try:
        t_name = tables[int(t_idx)-1]
    except:
        print("Scelta non valida!")
        return
        
    all_cols = get_columns(c, t_name)
    print(f"\nColonne in '{t_name}':")
    print(", ".join(all_cols))
    
    col_input = input("\nScrivi le colonne che vuoi vedere separate da virgola (es. id, title, year) oppure premi INVIO per vederle TUTTE:\n> ").strip()
    
    if not col_input:
        selected_cols = all_cols
    else:
        selected_cols = [col.strip() for col in col_input.split(',')]
        # Verifica colonne
        for col in selected_cols:
            if col not in all_cols:
                print(f"Errore: la colonna '{col}' non esiste!")
                return
                
    filter_input = input("\nVuoi filtrare i risultati? Scrivi la condizione (es. year > 2020 AND tier = 1) oppure premi INVIO per mostrare tutti i record:\n> ").strip()
    
    query = f"SELECT {', '.join(selected_cols)} FROM {t_name}"
    if filter_input:
        query += f" WHERE {filter_input}"
        
    print(f"\nEsecuzione: {query}")
    try:
        c.execute(query)
        rows = c.fetchall()
        draw_dynamic_table(selected_cols, rows)
    except sqlite3.Error as e:
        print(f"\n❌ Errore nella query SQL: {e}")
        
    conn.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUscita...")
