import sqlite3
import sys

def clearLikes(DBPath: str):
    conn = sqlite3.connect(DBPath)
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET id_likes = ""')
    cursor.execute('UPDATE articles SET likes = 0')
    conn.commit()

def clearUsers(DBPath: str):
    conn = sqlite3.connect(DBPath)
    cursor = conn.cursor()

    # remove all users 
    cursor.execute('DELETE FROM users')
    # reset autoincrement
    cursor.execute('UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = "users"')
    cursor.execute('UPDATE articles SET likes = 0')
    conn.commit()
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 clear.py <DBPath> <clear type>')
        exit()
        
    if sys.argv[2] == 'likes':
        clearLikes(sys.argv[1])
    elif sys.argv[2] == 'users':
        clearUsers(sys.argv[1])
    else:
        print('Usage: python3 clear.py <DBPath> <clear type>')
        print('clear type: likes / users')