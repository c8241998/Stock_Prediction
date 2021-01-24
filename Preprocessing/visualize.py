import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import datestr2num

def main():
    df = pd.read_pickle('./Preprocessing/file/stock_clean.pkl')
    items = [ 'Open', 'High', 'Low', 'Price', 'Volume','Weibo','Nasdaq']
    date = df['Date']

    print('\n\n\n------------------Visualization------------------\n')
    for index,item in enumerate(items):
        data = df[item]
        plt.figure(figsize=(15, 12))
        x_date = [datestr2num(i) for i in date]
        plt.xticks(rotation=45)
        # plt.ylabel(item)
        # plt.xlabel('Date')
        plt.xticks(fontsize=22)
        plt.yticks(fontsize=25)
        plt.grid()
        plt.plot_date(x_date, data, '-', label=item, color='b')
        plt.savefig('./Preprocessing/file/{}.jpg'.format('visual_'+item))

        print('plot has been stroed in [./Preprocessing/file/{}.jpg]'.format('visual_'+item))