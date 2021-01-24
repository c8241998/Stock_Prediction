import sqlite3
import numpy as np

def df_to_np(df):
    x_items = ['Nasdaq', 'Open', 'High', 'Low', 'Volume', 'Weibo']
    x, y, date = [], [], []
    for index, row in df.iterrows():
        temp = []
        y.append(row['Price'])
        date.append(row['Date'])
        for x_item in x_items:
            temp.append(row[x_item])
        x.append(temp)
    x, y = np.array(x), np.array(y)
    return x,y,date

def get_date_str(date):
    return date.strftime("%Y-%m-%d")

def execute_sql(sql):
    try:
        conn = sqlite3.connect('stock.db')
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception:
        print('already exists!')