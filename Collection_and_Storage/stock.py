import yfinance as yf
from sqlalchemy import create_engine
from Collection_and_Storage.utils import *


def download_stock_data():
    data = yf.download("AAPL", start="2017-04-02", end="2020-05-31")
    print('download finished')
    try:
        engine = create_engine('sqlite:///stock.db')
        data.to_sql('stock', con=engine)
    except ValueError:
        execute_sql('''DROP TABLE stock;''')
        data.to_sql('stock', con=engine)
    print('stock data has been stored in SQLite3 DB')

def main():
    print('\n\n\n------------------Collect and Store Stock Data------------------\n')
    # download original stock data to SQLite3 DB
    download_stock_data()
