import pickle
import matplotlib.pyplot as plt
from matplotlib.pylab import datestr2num
import pandas as pd
import numpy as np
from calendar import  mdays
import datetime as dt

def season(price,date):
    date = np.array(date).reshape(-1,1)
    price = price.reshape(-1,1)
    data = np.concatenate((date,price),axis=1)
    df = pd.DataFrame(data)
    df.rename(columns={0: 'datetime',1:'price'}, inplace=True)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime', drop=True)


    # fix missing value
    from_ = dt.datetime(2017, 4, 1)
    df.loc[from_] = df.loc['2017-04-03']['price']
    to_ = dt.datetime(2020, 5, 31)
    current = from_
    while current != to_:
        current = current + dt.timedelta(days=1)
        try:
            df.loc[current]
        except Exception:
            before = (current + dt.timedelta(days=-1)).strftime("%Y-%m-%d")
            null = current
            after = (current + dt.timedelta(days=2)).strftime("%Y-%m-%d")
            try:
                v=df.loc[before]['price']
            except Exception:
                v=df.loc[after]['price']
            df.loc[null] = v.item()
    df.sort_index(inplace=True)

    df = df.loc['2018-01-01':'2019-12-31']
    # pd.set_option('display.max_rows', None)
    # print(df)
    seasonal_cycle = df.rolling(window=30, center=True).mean().groupby(df.index.dayofyear).mean()
    q25 = df.rolling(window=30, center=True).mean().groupby(df.index.dayofyear).quantile(0.25)
    q75 = df.rolling(window=30, center=True).mean().groupby(df.index.dayofyear).quantile(0.75)

    ndays_m = mdays.copy()
    ndays_m[2] = 29
    ndays_m = np.cumsum(ndays_m)
    f, ax = plt.subplots(figsize=(10, 7))

    seasonal_cycle.plot(ax=ax, lw=2, color='b', legend=False)
    ax.fill_between(seasonal_cycle.index, q25.values.ravel(), q75.values.ravel(), color='b', alpha=0.3)
    ax.set_xticks(ndays_m + 15)
    ax.grid(ls=':')
    ax.set_xlabel('Day', fontsize=15)
    ax.set_ylabel('Stock Price (Normalized)', fontsize=15);
    ax.set_xlim(0, 365)
    [l.set_fontsize(13) for l in ax.xaxis.get_ticklabels()]
    [l.set_fontsize(13) for l in ax.yaxis.get_ticklabels()]

    plt.savefig('./Exploration/file/season.jpg')

    print('plot has been stored as [./Exploration/file/season.jpg]')

def main():
    f=open('Preprocessing/file/data.pkl', 'rb')
    X,price,date = pickle.load(f)

    print('\n\n\n------------------Trend Visualization------------------\n')
    # trend
    # visualize stock price
    plt.figure(figsize=(15, 8))
    x_date = [datestr2num(i) for i in date]
    plt.xticks(rotation=45)
    plt.ylabel('Stock Price (Normalized)')
    plt.xlabel('Date')
    plt.plot_date(x_date, price, '-', label='Stock Price', color='r')

    plt.savefig('./Exploration/file/visual_price.jpg')

    print('plot has been stored as [./Exploration/file/visual_price.jpg]')



    print('\n\n\n------------------Seasonality Exploration------------------\n')
    # seasonality
    season(price,date)

    print('\n\n\n------------------Unusual Behaviour------------------\n')
    print('Explanation with Trend Visualization and news')
    # unusual behaviour
    # 2018-9  -  2019-1
    # 2020-1  -  2020-5
    # nasdaq