# Stock Price Prediction
we have solved a real-life data acquisition and processing problem based on the stock price prediction. We have designed a solution including steps of finding the data, acquiring and storing the data, cleaning and preprocessing the data, training the model and finally analysing the data.

**Author: Zedong Chu**

**Course Code: ELEC0136 20/21**

## Requirements
- yfiance
- sqlalchemy
- pymongo
- paddlehub
- paddlepaddle
- pandas
- sqlite3
- scipy
- numpy
- matplotlib
- sklearn
- pickle
- seaborn
- calendar
- fbprophet

## Running

Before running this code, please make sure you have installed MongoDB and SQLite3 DB in your computer.
>Tips:
MongoDB:  https://www.mongodb.com/try#community
SQLite3 DB: https://www.sqlite.org/index.html
MongoDB is used to store the tweets data collected by our spider script, and the SQLite3 DB is used to store the final structured stock data.

To run this code, you just need: `python main.py`
