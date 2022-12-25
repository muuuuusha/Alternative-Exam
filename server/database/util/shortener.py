import sqlite3
import sys

def shortenDB(path: str, articlesCount: int) -> None:
    conn = sqlite3.connect(path)
    c = conn.cursor()
    
    # drop random articles to make DB of size articlesCount
    
    c.execute("SELECT id FROM articles")
    data = c.fetchall()
    data = data[articlesCount:]
    for i in data:
        c.execute("DELETE FROM articles WHERE id = ?", i)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 shortener.py <DB path> <articles count>")
        exit(1)
        
    if sys.argv[2].isdigit():
        articlesCount = int(sys.argv[2])
    
    shortenDB(sys.argv[1], articlesCount)
    
