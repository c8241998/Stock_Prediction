import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from Preprocessing.utils import df_to_np
import pickle

def pca(X,n_components=6):
    pca = PCA(n_components=n_components)
    newX = pca.fit_transform(X)
    # print(pca.explained_variance_ratio_)
    return newX
def main():
    print('\n\n\n------------------Transform------------------\n')

    # normalization
    df = pd.read_pickle('./Preprocessing/file/stock_clean.pkl')
    # z_scaler = lambda x: (x - np.mean(x)) / np.std(x)
    norm = lambda x:(x-np.min(x)) / (np.max(x)-np.min(x))
    df_norm = df[['Open', 'High', 'Low', 'Price', 'Volume','Weibo','Nasdaq']].apply(norm)
    df_norm = pd.concat([df[['Date']], df_norm], axis=1)
    df_norm.to_pickle('./Preprocessing/file/stock_normalized.pkl')

    print('normalization with min-max')
    print('data has been stored as [./Preprocessing/file/stock_normalized.pkl]')

    # pca

    # [6.46488718e-01 1.79490729e-01 1.55199738e-01 1.85773710e-02 1.30062453e-04 1.13381466e-04]
    X, Y, date = df_to_np(df_norm)
    X = pca(X,n_components='mle')
    f = open('Preprocessing/file/data.pkl','wb')
    pickle.dump((X,Y,date),f)

    print('pca for factors with externel data finished')
    print('data has been stored as [Preprocessing/file/data.pkl]')

    # print(Y)
    # print(X_with_externel.shape)
    # print(X_without_externel.shape)