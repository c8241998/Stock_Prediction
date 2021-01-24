import pandas as pd
import datetime as dt
from Collection_and_Storage.utils import *

def main():
    print('\n\n\n------------------Collect and Store Nasdaq Data------------------\n')
    print('nasdaq data has been downloaded from https://cn.investing.com/ as [./Collection_and_Storage/nasdaq.csv]')
    df = pd.read_csv('./Collection_and_Storage/nasdaq.csv')
    execute_sql('''alter table stock add column Nasdaq FLOAT;''')
    from_ = dt.datetime(2017, 4, 1)
    to_ = dt.datetime(2020, 5, 31)
    current = from_
    while current != to_:
        # saturday sunday no stock
        current = current + dt.timedelta(days=1)
        if current.weekday() >= 5:
            continue

        current_str = current.strftime("%Y-%m-%d")
        try:
            nasdaq_point = df[df['Date']==current_str]['Close'].item()
        except ValueError:
            nasdaq_point = 0
        execute_sql('''update stock set Nasdaq = {} where Date like '%{}%'; '''.format(nasdaq_point,
                                                                                      current.strftime("%Y-%m-%d")))

    print('nasdaq data has been stored in SQLite3 DB')