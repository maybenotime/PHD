import json
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score
import re
import numpy as np

data_path = './verified_data_after_check.json'
record_path = './RV_QA/RV_qa_result.json'

label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data

def get_label(data):
    all_label = []
    for key,value in data.items():
        for entry in value:
            all_label.append(entry['label'])
            
    return all_label



def get_revised_predict_detail(data,label):           #detail版本
    all_predict = []
    for record,gt in zip(data,label):
        entity = record['entity'].split('(')[0].strip()     #去掉括号注释以防匹配失败
        answer = record['answer']       #直接取answer做字符串匹配，不要最后一步
        percent = re.search('(\d*)%',answer)
        if ('100%' in answer or 'perfect match' in answer or 'meets all' in answer or 'matches all' in answer) and 'except' not in answer:    #百分百符合要求
            if entity.lower() in answer.lower() and len(entity) >= 5:    #实体符合即正确，这个长度限制是怕有些很短的实体缩写小写后直接被误打误撞匹配到
                label = 'factual'
            else:
                if entity in answer:        #这是捕获那些长度小于5的在上一轮被略过的正确匹配
                    label = 'factual'
                else:                       #这边就是完全没匹配上的
                    label = 'non-factual'
        else:
            if entity.lower() not in answer.lower():     #没匹配到就是错误的
                label = 'non-factual'
            else:      #实体符合，且概率大于80,也算正确
                if percent is not None:
                    if int(percent.groups()[0]) >= 80:
                        label = 'factual'
                    else:
                        label = 'non-factual'
                else:               #未找到概率一般就是完美匹配的情况
                    label = 'factual'
                        
          
        all_predict.append(label)
    return all_predict

def get_revised_predict(data):          #其他版本，不用判断百分比
    all_predict = []
    for record in data:
        entity = record['entity'].split('(')[0].strip()     #去掉括号
        answer = record['answer']       #直接取answer做字符串匹配，不要最后一步
        if entity.lower() in answer.lower():
            label = 'factual'
        else:
            label = 'non-factual'
        all_predict.append(label)
    
    return all_predict


  

#以下是计算PHD dataset的代码 
        
data = read_data(data_path)
record = read_data(record_path)
label_list = get_label(data)
predict_list = get_revised_predict(record)


map_label = [label_mapping[i] for i in label_list]
map_predict = [label_mapping[i] for i in predict_list]

f1 = f1_score(map_label, map_predict)
p = precision_score(map_label, map_predict)
r = recall_score(map_label, map_predict)

print("all_metric:")
print(f1,p,r)


f1_10w = f1_score(map_label[100:200],map_predict[100:200])
p_10w = precision_score(map_label[100:200],map_predict[100:200])
r_10w = recall_score(map_label[100:200],map_predict[100:200])
print("10w_metric:")
print(f1_10w,p_10w,r_10w)

f1_1000w = f1_score(map_label[:100],map_predict[:100])
p_1000w = precision_score(map_label[:100],map_predict[:100])
r_1000w = recall_score(map_label[:100],map_predict[:100])
print("1000w_metric:")
print(f1_1000w,p_1000w,r_1000w)

f1_1y = f1_score(map_label[200:],map_predict[200:])
p_1y = precision_score(map_label[200:],map_predict[200:])
r_1y = recall_score(map_label[200:],map_predict[200:])
print("1y_metric:")
print(f1_1y,p_1y,r_1y)
