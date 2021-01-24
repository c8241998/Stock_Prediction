from scipy.stats import pearsonr
import seaborn as sn
import pickle
import matplotlib.pyplot as plt

def feature_corr(X):

    # boxplot
    matrix = []
    for factor1 in X.T:
        temp = []
        for factor2 in X.T:
            feature_corr, _ = pearsonr(factor1, factor2)
            temp.append(feature_corr)
        matrix.append(temp)

    feature_corr_map = sn.heatmap(matrix, annot=True, fmt='g')
    fig = feature_corr_map.get_figure()
    fig.savefig('Exploration/file/feature_corr/map.jpg')

    print('boxplot has been stored in [./Exploration/file/feature_corr/]')

    # scatterplot
    for i,factor1 in enumerate(X.T):
        for j,factor2 in enumerate(X.T):
            if i>=j:
                continue
            plt.clf()
            plt.scatter(factor1, factor2)
            plt.title('Values of two factors')
            plt.xlabel('factor {} '.format(i+1))
            plt.ylabel('factor {} '.format(j+1))
            plt.savefig('Exploration/file/feature_corr/scatter_{}_{}.jpg'.format(i+1,j+1))

    print('scatterplot has been stored in [./Exploration/file/feature_corr/]')

def price_externel_corr(X,price):

    # scatterplot
    for i,factor in enumerate(X.T):
        plt.clf()
        plt.scatter(price, factor)
        plt.title('Values of the stock price and factor{}'.format(i+1))
        plt.xlabel('stock price')
        plt.ylabel('factor {} '.format(i + 1))
        plt.savefig('Exploration/file/price_corr/scatter_{}.jpg'.format(i + 1))

        corr, _ = pearsonr(price, X[:,i])
        print('corr between factor_{} and price is {}'.format(i,corr))
        # 0.9970

    print('scatterplot has been stored in [./Exploration/file/price_corr/]')

def main():


    f = open('Preprocessing/file/data.pkl', 'rb')
    X, price, date = pickle.load(f)

    print('\n\n\n------------------Correlation among features------------------\n')
    feature_corr(X)

    print('\n\n\n------------------Correlation between price and features------------------\n')
    price_externel_corr(X,price)