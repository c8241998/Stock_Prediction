import sqlite3

def execute_sql(sql):
    try:
        conn = sqlite3.connect('stock.db')
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception:
        print('already exists!')