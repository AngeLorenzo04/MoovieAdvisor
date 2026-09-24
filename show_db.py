import sqlite3

def draw_table():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT id, substr(title, 1, 30), year, tier, mood_tag FROM movies ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    
    print("┌────┬────────────────────────────────┬──────┬──────┬───────────────┐")
    print("│ id │             Titolo             │ Anno │ tier │     Mood      │")
    print("├────┼────────────────────────────────┼──────┼──────┼───────────────┤")
    
    for row in rows:
        r_id = str(row[0]).ljust(2)
        title = str(row[1]).ljust(30)
        year = str(row[2]).ljust(4)
        tier = str(row[3]).ljust(4)
        mood = str(row[4]).ljust(13)
        print(f"│ {r_id} │ {title} │ {year} │ {tier} │ {mood} │")
        
    print("└────┴────────────────────────────────┴──────┴──────┴───────────────┘")
    conn.close()

if __name__ == "__main__":
    draw_table()
