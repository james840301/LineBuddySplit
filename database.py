import sqlite3

# 建立資料庫連接
conn = sqlite3.connect('accounting.db', check_same_thread=False)
cursor = conn.cursor()

# 創建表格（如果尚未存在）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        amount INTEGER NOT NULL,
        date TEXT DEFAULT (datetime('now', 'localtime'))
    )
''')
conn.commit()

# 函數：插入新記錄
def insert_transaction(category, name, amount):
    cursor.execute('INSERT INTO transactions (category, name, amount) VALUES (?, ?, ?)', (category, name, amount))
    conn.commit()

# 函數：查詢所有記錄
def get_all_transactions():
    cursor.execute('SELECT * FROM transactions')
    return cursor.fetchall()

# 關閉連接（可選，如果需要在最後結束程序時執行）
def close_connection():
    cursor.close()
    conn.close()
