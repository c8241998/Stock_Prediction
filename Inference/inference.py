from Inference import lstm_base,lstm_externel,prophet
import matplotlib.pyplot as plt
from matplotlib.pylab import datestr2num
import pickle
from Inference.utils import get_df_to_plot,create_joint_plot
import seaborn as sns

def main():
    f = open('Preprocessing/file/data.pkl', 'rb')
    X, price_gt, date = pickle.load(f)
    print(price_gt.shape)

    # train our lstm model
    window=20
    date_lstm = date[window:]
    epochs = 100
    price_base = lstm_base.pipeline(epochs=epochs,window=window)
    price_externel = lstm_externel.pipeline(epochs=epochs,window=window)
    f = open('Inference/file/pred_price_temp.pkl', 'wb')
    pickle.dump((price_base, price_externel), f)
    # f = open('Inference/file/pred_price_temp.pkl', 'rb')
    # price_base, price_externel = pickle.load(f)


    #  create joint plot for lstm base
    df_base = get_df_to_plot(price_base,price_gt[window:],date[window:])
    plot_train = create_joint_plot(df_base.loc[:'2020-04-30', :], title='Train set')
    plot_train.savefig('./Inference/file/joint_plot_base_train.jpg')
    plot_test = create_joint_plot(df_base.loc['2020-05-01':, :], title='Test set')
    plot_test.savefig('./Inference/file/joint_plot_base_test.jpg')

    #  create joint plot for lstm externel
    df_externel = get_df_to_plot(price_externel, price_gt[window:], date[window:])
    plot_train = create_joint_plot(df_externel.loc[:'2020-04-30', :], title='Train set')
    plot_train.savefig('./Inference/file/joint_plot_externel_train.jpg')
    plot_test = create_joint_plot(df_externel.loc['2020-05-01':, :], title='Test set')
    plot_test.savefig('./Inference/file/joint_plot_externeltest.jpg')


    # plot prediction and groundtruth
    plt.figure(figsize=(15, 8))
    date_gt = [datestr2num(i) for i in date]
    date_lstm = [datestr2num(i) for i in date_lstm]
    plt.xticks(rotation=45)
    plt.ylabel('Stock Price (Normalized)')
    plt.xlabel('Date')
    plt.plot_date(date_gt, price_gt, '-', label='Groung Truth', color='r')
    plt.plot_date(date_lstm, price_base, '-', label='lstm without externel data', color='b')
    plt.plot_date(date_lstm, price_externel, '-', label='lstm with externel data', color='m')
    plt.axvline(x=datestr2num('2020-05-01'), c="k", ls="--", lw=1)
    plt.legend()
    plt.savefig('./Inference/file/prediction.jpg')

    # uncertainty interval
    # prophet.main(price_base,price_externel,window=window)


    # residual distribution
    dfs = [df_base,df_externel]
    for i,df in enumerate(dfs):
        f, ax = plt.subplots(figsize=(8, 8))
        df_yhat = df.loc['2020-05-01':, 'yhat']
        df_y = df.loc['2020-05-01':, 'y']
        # df_yhat = df.loc[:'2020-05-01', 'yhat']
        # df_y = df.loc[:'2020-05-01', 'y']
        df_residual = df_yhat-df_y
        sns.distplot(df_residual, ax=ax, color='0.4')
        ax.grid(ls=':')
        ax.set_xlabel('residuals', fontsize=15)
        ax.set_ylabel("normalised frequency", fontsize=15)
        ax.grid(ls=':')

        [l.set_fontsize(13) for l in ax.xaxis.get_ticklabels()]
        [l.set_fontsize(13) for l in ax.yaxis.get_ticklabels()];

        from scipy.stats import skew
        ax.text(0.05, 0.9, "Skewness = {:+4.2f}\nMedian = {:+4.2f}\nMean = {:4.2f}". \
                format(skew(df_residual), df_residual.median(), df_residual.mean()), \
                fontsize=14, transform=ax.transAxes)

        ax.axvline(0, color='0.4')

        ax.set_title('Residuals distribution (test set)', fontsize=17)

        if i==0:
            f.savefig('./Inference/file/residual_distribution_base.jpg')
        else:
            f.savefig('./Inference/file/residual_distribution_externel.jpg')