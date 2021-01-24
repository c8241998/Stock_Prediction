import paddle
from paddle.io import Dataset
import pickle
import numpy as np
from Inference.utils import MSE

class MyDataset(Dataset):
    def __init__(self,window,mode='train'):
        super(MyDataset, self).__init__()
        dir_pkl = 'Preprocessing/file/data.pkl'
        f = open(dir_pkl, 'rb')
        X, price, date = pickle.load(f)
        self.data=[]
        if mode=='train':
            for i,day in enumerate(date):
                if i<window or '2020-05' in day:
                    continue
                sample = self.get_sample(price,window,i)
                self.data.append([
                    sample[0],sample[1]
                ])
        else:
            for i, day in enumerate(date):
                if i < window or not '2020-05' in day:
                    continue
                sample = self.get_sample(price, window, i)
                self.data.append([
                    sample[0],sample[1]
                ])
    def get_sample(self,price, window,i):
        prices = price[i - window:i].astype(np.float32)
        prices = np.expand_dims(prices,axis=-1)
        return prices , price[i].astype(np.float32)

    def __getitem__(self, index):
        data = self.data[index][0]
        label = self.data[index][1]
        return data,label
    def __len__(self):
        return len(self.data)

class rnn(paddle.nn.Layer):
    def __init__(self,window):
        super(rnn, self).__init__()
        self.lstm = paddle.nn.LSTM(1,1,2)
        self.nn = paddle.nn.Sequential(
            paddle.nn.Flatten(),
            paddle.nn.Linear(window,1),
            paddle.nn.Sigmoid()
        )
    def forward(self,inputs):
        x,_ = self.lstm(inputs)
        x = self.nn(x)
        return x

def pipeline(window,epochs=100):
    train_dataset = MyDataset(mode='train',window=window)
    val_dataset = MyDataset(mode='val',window=window)

    # for data,label in train_dataset:
    #     print(data.shape,label)

    rnn_ = rnn(window)
    model = paddle.Model(rnn_)
    model.prepare(optimizer=paddle.optimizer.Adam(parameters=rnn_.parameters()),
                  loss=paddle.nn.MSELoss(),
                  metrics=MSE()
                  )
    model.fit(train_data=train_dataset,
              eval_data=val_dataset,
              epochs=epochs,
              batch_size=1,
              verbose=1)
    eval_result = model.evaluate(val_dataset, verbose=1)

    prediction = []
    pre = model.predict(train_dataset)
    for i, data in enumerate(train_dataset):
        prediction.append(pre[0][i][0][0])
    pre = model.predict(val_dataset)
    for i, data in enumerate(val_dataset):
        prediction.append(pre[0][i][0][0])

    return prediction



    # x=paddle.randn([16,10,1])
    # y=rnn_(x)
    # print(y.shape)

    # loss:0.0069  mse:0.00548357