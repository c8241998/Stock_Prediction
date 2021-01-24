from Collection_and_Storage import weibo,stock,nasdaq
from Preprocessing import clean,visualize,transform
from Exploration import timeseries,correlation,hypothesis
from Inference import inference
def collect_store_data():
    stock.main()
    weibo.main()
    nasdaq.main()

def preprocessing_data():
    clean.main()
    visualize.main()
    transform.main()

def explore_data():
    timeseries.main()
    correlation.main()
    hypothesis.main()

def inference_data():
    inference.main()

if __name__=='__main__':

    collect_store_data()
    preprocessing_data()
    explore_data()
    inference_data()
