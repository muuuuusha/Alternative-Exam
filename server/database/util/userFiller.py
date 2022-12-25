import sqlite3
import sys

# fill users table with 1000 users with random names and passwords

def addUsers(DBPath: str, amount: int):
    conn = sqlite3.connect(DBPath)
    cursor = conn.cursor()
    
    for i in range(1, amount+1):
        username = 'user' + str(i)
        password = 'pass' + str(i)
        likes = ''
        cursor.execute('INSERT INTO users (username, password, id_likes) VALUES (?, ?, ?)', (username, password, likes))
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 userFiller.py <DBPath> <amount>')
        exit()
    addUsers(sys.argv[1], int(sys.argv[2])) 