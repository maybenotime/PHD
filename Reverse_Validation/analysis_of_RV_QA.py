#Suggestion by Reviewer JYbz
#perform an analysis of how many questions lost key information in the RV-QG method and how many bad cases are caused by missing key information
import json
import random


data_path = '../process_annotated_data/data_store/verified_data_after_check.json'
qg_record_path = './our_dataset_qg_record.json'


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

def analysis(data,record):
    for data_entry,record_entry in zip(data,record):
        print('###############################')
        print(data_entry['entity'])
        print(record_entry['entity'])
        print(data_entry['AI'])
        print(data_entry['label'])
        print(record_entry['question'])
        print(record_entry['answer'])
        print('###############################')
    
data = read_data(data_path)
qa_record = read_data(qg_record_path)
data_list = flatten_data(data)
random.seed(42)
random.shuffle(data_list)
random.seed(42)
random.shuffle(qa_record)
analysis(data_list[:30],qa_record[:30])