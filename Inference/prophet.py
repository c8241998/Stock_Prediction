import pandas as pd
import pickle
from fbprophet import Prophet
import numpy as np
import matplotlib.pyplot as plt


def train_test_split(data):
    train = data.set_index('ds').loc[:'2020-04-30', :].reset_index()
    test = data.set_index('ds').loc['2020-05-01':, :].reset_index()
    return train, test


def make_predictions_df(forecast, data_train, data_test):
    """
    Function to convert the output Prophet dataframe to a datetime index and append the actual target values at the end
    """
    forecast.index = pd.to_datetime(forecast.ds)
    data_train.index = pd.to_datetime(data_train.ds)
    data_test.index = pd.to_datetime(data_test.ds)
    data = pd.concat([data_train, data_test], axis=0)
    forecast.loc[:, 'y'] = data.loc[:, 'y']

    return forecast


def plot_predictions(forecast,price_base,price_externel,window):
    """
    Function to plot the predictions
    """

    plt.figure(figsize=(15, 8))
    plt.ylim(0,1)

    train = forecast.loc[:'2020-04-30', :]
    plt.plot(train.index, train.yhat, color='steelblue', lw=0.5,label='predicted value of fbprophet model before 2020-05-01')
    plt.fill_between(train.index, train.yhat_lower, train.yhat_upper, color='steelblue', alpha=0.3,label='predicted uncertainty interval of fbprophet model before 2020-05-01')

    test = forecast.loc['2020-05-01':, :]
    plt.plot(test.index, test.yhat, color='coral', lw=0.5, label = 'predicted value of fbprophet model after 2020-05-01')
    plt.fill_between(test.index, test.yhat_lower, test.yhat_upper, color='coral', alpha=0.3,label='predicted uncertainty interval of fbprophet model after 2020-05-01')
    plt.axvline(forecast.loc['2020-05-01', 'ds'], color='k', ls='--', alpha=0.7)
    plt.grid(ls=':', lw=0.5)

    plt.ylabel('Stock Price (Normalized)')
    plt.xlabel('Date')


    # plot externel
    line1, = plt.plot(train.index[window:], price_externel[:-20], color='k', marker='.', alpha=0.3,
                      label='predicted value of our LSTM model with externel data')
    line2, = plt.plot(test.index, price_externel[-20:], color='k', marker='.', alpha=0.3)
    plt.legend()
    plt.savefig('./Inference/file/uncertainty_externel.jpg')

    ax=plt.gca()
    ax.lines.remove(line1)
    ax.lines.remove(line2)

    # plot base
    plt.plot(train.index[window:], price_base[:-20], color='k', marker='.', alpha=0.3,
                      label='predicted value of our LSTM model without externel data')
    plt.plot(test.index, price_base[-20:], color='k', marker='.', alpha=0.3)

    plt.legend()
    plt.savefig('./Inference/file/uncertainty_base.jpg')




def main(price_base,price_externel,window):
    print('\n\n\n------------------Prophet Uncertainty Interval------------------\n')
    f = open('Preprocessing/file/data.pkl', 'rb')
    X, price, date = pickle.load(f)

    date = np.array(date).reshape(-1, 1)
    price = price.reshape(-1, 1)
    # data = np.concatenate((date, price, X), axis=1)
    data = np.concatenate((date, price), axis=1)
    df = pd.DataFrame(data)
    df.rename(columns={0: 'ds', 1: 'y'}, inplace=True)
    # df.rename(columns={0: 'ds', 1: 'y', 2: 'f1', 3: 'f2', 4: 'f3', 5: 'f4'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])

    train, test = train_test_split(data=df)

    m = Prophet(
                interval_width=0.95,
                seasonality_mode='multiplicative',
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True
                )
    # m.add_regressor('f1', mode='multiplicative')
    # m.add_regressor('f2', mode='multiplicative')
    # m.add_regressor('f3', mode='multiplicative')
    # m.add_regressor('f4', mode='multiplicative')

    m.fit(train)
    future = df.drop('y',1)
    forecast = m.predict(future)

    f = m.plot_components(forecast, figsize=(12, 16))
    f.savefig('./Inference/file/base_components.jpg')

    result = make_predictions_df(forecast, train, test)
    result.loc[:, 'yhat'] = result.yhat.clip(lower=0)
    result.loc[:, 'yhat_lower'] = result.yhat_lower.clip(lower=0)
    result.loc[:, 'yhat_upper'] = result.yhat_upper.clip(lower=0)

    result = result.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
    # pd.set_option('display.max_rows', None)

    plot_predictions(result,price_base,price_externel,window)



    # result['y'] = result['y'].astype(np.float32)

    # plot_train = create_joint_plot(result.loc[:'2020-04-30', :], title='Train set')
    # plot_train.savefig('./Inference/file/base_train.jpg')
    #
    # plot_test = create_joint_plot(result.loc['2020-05-01':, :], title='Test set')
    # plot_test.savefig('./Inference/file/base_test.jpg')
