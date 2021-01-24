import pandas as pd
import pickle
from scipy.stats import chi2_contingency
from scipy.stats import chi2

def get_trend(list):
    list = [list[i] - list[i - 1] for i in range(1, len(list))]
    list[0] = 0
    list = [1 if x > 0 else 0 for x in list]
    return list

def main():
    print('\n\n\n------------------Chi-Square Test------------------\n')

    f=open('Preprocessing/file/data.pkl', 'rb')
    X,price,date = pickle.load(f)
    X=X.T

    price = get_trend(price)

    for i,factor in enumerate(X):
        factor = get_trend(factor)
        temp = [price[i]*10+factor[i] for i in range(len(price))]
        data = [[temp.count(11),temp.count(10)],[temp.count(1),temp.count(0)]]
        df = pd.DataFrame(data)
        df.rename(columns={0: 'factor{}_up'.format(i), 1: 'factor{}_down'.format(i)}, inplace=True)
        df.rename(index={0: 'price{}_up'.format(i), 1: 'price{}_down'.format(i)}, inplace=True)
        print(df)
        stat, p, dof, expected = chi2_contingency(df)
        print("statistic", stat)
        print("p-value", p)
        print("degres of fredom: ", dof)
        print("table of expected frequencies\n", expected)

        prob = 0.90
        critical = chi2.ppf(prob, dof)
        if abs(stat) >= critical:
            print('factor{} and price are Dependent (reject H0)\n\n\n'.format(i))
        else:
            print('factor{} and price are Independent (fail to reject H0)\n\n\n'.format(i))