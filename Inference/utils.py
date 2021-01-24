from paddle.metric import Metric
import numpy as np
import seaborn as sns
import pandas as pd

class MSE(Metric):

    def __init__(self, name='mse', *args, **kwargs):
        super(MSE, self).__init__(*args, **kwargs)
        self.sum = 0
        self.cnt = 0
        self._name = name

    def update(self, preds, labels):

        sample_num = labels.shape[0]

        for i in range(sample_num):
            pred = preds[i]
            label = labels[i]
            self.sum = self.sum + (pred - label) * (pred - label)
            self.cnt = self.cnt + 1
    def reset(self):
        """
        Resets all of the metric state.
        """
        self.sum = 0
        self.cnt = 0

    def accumulate(self):

        return self.sum / (float)(self.cnt)

    def name(self):
        """
        Returns metric name
        """
        return self._name


def create_joint_plot(forecast, x='yhat', y='y', title=None):
    g = sns.jointplot(x='yhat', y='y', data=forecast, kind="reg", color="b")
    g.fig.set_figwidth(8)
    g.fig.set_figheight(8)

    ax = g.fig.axes[1]
    if title is not None:
        ax.set_title(title, fontsize=16)

    ax = g.fig.axes[0]
    ax.text(0.1, 0.8, "R = {:+4.2f}".format(forecast.loc[:, ['y', 'yhat']].corr().iloc[0, 1]), fontsize=16)
    ax.set_xlabel('Predictions', fontsize=15)
    ax.set_ylabel('Observations', fontsize=15)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(ls=':')
    [l.set_fontsize(13) for l in ax.xaxis.get_ticklabels()]
    [l.set_fontsize(13) for l in ax.yaxis.get_ticklabels()];

    ax.grid(ls=':')
    return g

def get_df_to_plot(pre,gt,date):

    date = np.array(date).reshape(-1, 1)
    gt = np.array(gt).reshape(-1, 1)
    pre = np.array(pre).reshape(-1,1)
    data = np.concatenate((date, gt, pre), axis=1)
    df = pd.DataFrame(data)
    df.rename(columns={0: 'ds', 1: 'y', 2:'yhat'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    df['y'] = df['y'].astype(np.float32)
    df['yhat'] = df['yhat'].astype(np.float32)
    df.index = pd.to_datetime(df.ds)

    return df
