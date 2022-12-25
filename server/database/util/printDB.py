import sqlite3
import sys

def printUsers(DBPath: str, n: int, onlyLiked: bool = False):
    conn = sqlite3.connect(DBPath)
    cursor = conn.cursor()

    if onlyLiked:
        cursor.execute('SELECT * FROM users WHERE id_likes != ""')
    else:
        cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    
    if len(rows) == 0:
        print('No users')

    for row in rows[:n]:
        print(row)
        
    conn.close()

def printArticles(DBPath: str, n: int, onlyLiked: bool = False):
    conn = sqlite3.connect(DBPath)
    cursor = conn.cursor()
    
    if onlyLiked:
        cursor.execute('SELECT * FROM articles WHERE likes > 0')
    else:
        cursor.execute('SELECT * FROM articles')
    rows = cursor.fetchall()
    
    if len(rows) == 0:
        print('No articles')
    for row in rows[:n]:
        print(f'Article {row[0]}: \n\tfilename: {row[1]}\n\ttitle: {row[2]}\n\tauthor: {row[3]}\n\tlikes: {row[4]}')
        
    conn.close()
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python3 printDB.py <DBPath> <table> <max rows> [onlyLiked]')
        exit()
        
    onlyLiked = (len(sys.argv) == 5 and sys.argv[4] == 'onlyLiked')
    
    if sys.argv[2] == 'users':
        printUsers(sys.argv[1], int(sys.argv[3]), onlyLiked)
    elif sys.argv[2] == 'articles':
        printArticles(sys.argv[1], int(sys.argv[3]), onlyLiked)
    elif sys.argv[2] == 'all':
        print('Users:')
        printUsers(sys.argv[1], int(sys.argv[3]), onlyLiked)
        print('Articles:')
        printArticles(sys.argv[1], int(sys.argv[3]), onlyLiked)