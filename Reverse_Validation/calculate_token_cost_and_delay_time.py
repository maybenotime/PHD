from detection_components import *
from sklearn.metrics import f1_score
import json
from tqdm import tqdm
import random


data_path = './process_annotated_data/data_store/verified_data_after_check.json'


def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data

def flatten_data(data):
    flatten_data = []
    for key,value in data.items():
        for entry in value:
            flatten_data.append(entry)   
    
    return flatten_data

def timer(func):                    #计算函数运行时长的装饰器
    def func_wrapper(*args, **kwargs):
        from time import time
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        time_spend = time_end - time_start
        print('%s cost time: %.3f s' % (func.__name__, time_spend))
        return result
    return func_wrapper



@timer
def TIME_RV_RUN(test_set):            #使用RV跑三十条所需时间
    for entry in tqdm(test_set):
        result = RV_QG_token_cost(entry['entity'],entry['AI'])
    

data = read_data(data_path)
data_list = flatten_data(data)
random.seed(42)
random.shuffle(data_list)
test_set = data_list[:30]
TIME_RV_RUN(test_set)