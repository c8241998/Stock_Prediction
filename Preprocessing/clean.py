import pandas.io.sql as sql
import sqlite3
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import datestr2num
from sklearn.ensemble import RandomForestRegressor

def detect_outlier(df,figpath):

    weibo = df['Weibo']
    nasdaq = df['Nasdaq']
    open = df['Open']
    high = df['High']
    low = df['Low']
    volume = df['Volume']
    AdjClose = df['Adj Close']

    date = df['Date']
    z_weibo = np.abs(stats.zscore(weibo))
    z_nasdaq = np.abs(stats.zscore(nasdaq))
    z_open = np.abs(stats.zscore(open))
    z_high = np.abs(stats.zscore(high))
    z_low = np.abs(stats.zscore(low))
    z_volume = np.abs(stats.zscore(volume))
    z_AdjClose = np.abs(stats.zscore(AdjClose))

    plt.figure(figsize=(20, 15))
    x_date = [datestr2num(i) for i in date]
    plt.xticks(rotation=45)
    plt.ylim([0, 6])
    plt.xlabel('Date',fontsize=22)
    plt.ylabel('Z score',fontsize=22)
    plt.grid()
    plt.plot_date(x_date, z_weibo, '-', label="weibo", color='b')
    plt.plot_date(x_date, z_nasdaq, '-', label="nasdaq", color='c')
    plt.plot_date(x_date, z_open, '-', label="open", color='g')
    plt.plot_date(x_date, z_high, '-', label="high", color='m')
    plt.plot_date(x_date, z_low, '-', label="low", color='y')
    plt.plot_date(x_date, z_volume, '-', label="volume", color='r')
    plt.plot_date(x_date, z_AdjClose, '-', label="AdjClose", color='k')
    plt.legend(prop={'size':25})
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=25)
    plt.savefig(figpath)
    print('current fig (dealt with outliers) stored in [{}]'.format(figpath))

    threshold = 3
    outlier_loc = np.where(z_weibo > threshold)[0]

    return outlier_loc

def solve_outlier(df,outlier_loc):
    x_items = ['Nasdaq','Open','High','Low','Volume','Adj Close']
    x,y=[],[]
    for index,row in df.iterrows():
        if index in outlier_loc:
            continue
        temp=[]
        y.append(row['Weibo'])
        for x_item in x_items:
            temp.append(row[x_item])
        x.append(temp)
    x,y=np.array(x),np.array(y)
    regr = RandomForestRegressor()
    regr.fit(x, y)

    for index in outlier_loc:
        x = []
        for x_item in x_items:
            x.append(df.loc[index,x_item])
        y = regr.predict(np.array([x])).item()
        df.loc[index,'Weibo'] = y

    print('current outliers solved successfully with random forest regressor')
    return df

def main():
    print('\n\n\n------------------Clean Data------------------\n')

    conn = sqlite3.connect('stock.db')
    df = sql.read_sql('select * from stock',conn)

    # delete close
    df = df.drop(labels='Close',axis=1)
    print('delete Close Column')

    # fix date format
    for index,row in df.iterrows():
        df.loc[index,'Date'] = row['Date'][:10]
    print('fix date format')

    # missing value of weibo
    for index,row in df.iterrows():
        if(row['Weibo']==0):
            df.loc[index, 'Weibo'] = (df.loc[index-1, 'Weibo'] + df.loc[index+1, 'Weibo'])/2
    print('fix missing value of weibo')

    # detect outlier
    iter=0
    while 1:
        outlier_loc = detect_outlier(df,figpath='./Preprocessing/file/outlier{}.jpg'.format(iter))
        print('iter{}:  detect outliers in location '.format(iter), outlier_loc)

        if len(outlier_loc)==0:
            break
        iter = iter + 1
        df = solve_outlier(df,outlier_loc)

            # 2018-03-06
            # 2019-02-22
            # 2019-12-04
            # 2020-04-06

    # change column name of 'Adj Close'
    df.rename(columns={'Adj Close':'Price'},inplace=True)
    df.to_pickle('./Preprocessing/file/stock_clean.pkl')
    print('change column name of Adj Close to Price')