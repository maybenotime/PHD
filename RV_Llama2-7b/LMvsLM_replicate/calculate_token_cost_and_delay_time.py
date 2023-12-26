import json
from tqdm import tqdm
from LM_vs_LM import *
import random


data_path = '../process_annotated_data/data_store/verified_data_after_check.json'


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

def detect_hal(entity,claim):
    lawyer = exmainer(claim)
    suspect = Suspect(entity, claim)
    question = lawyer.Setup()       #提问
    trigger = True      #是否继续询问
    count = 1           #询问轮次计数
    while(trigger):
        count += 1
        answer = suspect.answer_without_history(question)  #回答
        flag = lawyer.check_follow_up_question(answer) #是否继续提问？
        if 'No' in flag or count == 5:                #不问了，直接出结论
            lawyer_history = lawyer.decision()
            trigger = False             #退出询问
        else:                           #继续问
            question = lawyer.ask_continue()
            
    return lawyer_history[-1]['content'],lawyer_history

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
def TIME_RUN(test_set):            #使用跑三十条所需时间
    for entry in tqdm(test_set):
        label_content,history = detect_hal(entry['entity'],entry['AI'])
    

data = read_data(data_path)
data_list = flatten_data(data)
random.seed(42)
random.shuffle(data_list)
test_set = data_list[:30]
TIME_RUN(test_set)
