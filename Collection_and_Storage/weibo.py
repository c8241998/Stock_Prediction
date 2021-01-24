import os
from pymongo import MongoClient
import datetime as dt
import paddlehub as hub
from Collection_and_Storage.utils import *

def get_tweets_from_mongo():

    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client['weibo_spider']
    tweets = db["Tweets"]

    return tweets

def run_spider():
    os.system('python ./Collection_and_Storage/weibo_spider/weibospider/run_spider.py tweet')

def judge_tweets(tweets,senta):
    texts = []
    for tweet in tweets:
        texts.append(tweet['content'])

    try:
        results = senta.sentiment_classify(texts=texts)
    except ValueError:
        return 0

    cnt = len(texts)
    sum = 0
    for result in results:
        positive = result['positive_probs']
        negative = result['negative_probs']
        sum = sum + positive - negative

    return sum / cnt



def analyze_tweets(tweets):
    print('start to analyze tweets\n')
    execute_sql('''alter table stock add column Weibo FLOAT;''')

    from_ = dt.datetime(2017, 4, 1)
    to_ = dt.datetime(2020, 5, 31)
    current = from_
    senta = hub.Module(name="senta_lstm")
    senta.__init__()
    while current!=to_:
        # saturday sunday no stock
        current = current + dt.timedelta(days=1)
        if current.weekday()>=5:
            continue
        tweets_current = tweets.find({'created_at':{"$regex": current.strftime("%Y-%m-%d")}})
        sentimental_point = judge_tweets(tweets_current,senta)

        execute_sql('''update stock set Weibo = {} where Date like '%{}%'; '''.format(sentimental_point,current.strftime("%Y-%m-%d")))

        print(current,"   ",sentimental_point)



def main():
    run_spider()
    print('\n\n\n------------------Collect and Store Weibo Data------------------\n')
    # print('tweets has been collected before in MongoDB. If you want to re-collect them or first run this script, just uncomment run_spider function in weibo.py.')
    tweets = get_tweets_from_mongo()
    print('tweets count: ',tweets.count_documents({}))
    analyze_tweets(tweets)
    print('analyze sentimental point of tweets finished')

def delete_all():
    tweets = get_tweets_from_mongo()
    tweets.delete_many({})