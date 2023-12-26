import json
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score
import re
import numpy as np

data_path = '../PHD_benchmark.json'   #PHD benchmark
wiki_bio_dataset = '../LMvsLM_replicate/Self_check_gpt_data/new_wikibio_data.json'

wikibio_qg_record_path = './wiki_bio_qg_record.json'
wikibio_em_record_path = './wiki_bio_em_record.json'

qg_record_path = './our_dataset_qg_record.json'
em_record_path = './our_dataset_em_record.json'

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

def get_wikibio_ratio(data):     #获得幻觉比例
    all_ratio = []
    for entry in data:
        all_ratio.append(entry['ratio'])
    
    return all_ratio


def get_em_predict(data):           #RV-EM version
    all_predict = []
    for record in data:
        entity = record['entity'].split('(')[0].strip()     #去掉括号注释以防匹配失败
        answer = record['answer']       
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
            else:      #实体符合，且概率大于80
                if percent is not None:
                    if int(percent.groups()[0]) >= 80:
                        label = 'factual'
                    else:
                        label = 'non-factual'
                else:               #未输出概率一般就是完美匹配的情况
                    label = 'factual'
                        
          
        all_predict.append(label)
    return all_predict

def get_qg_predict(data):          #RV-QG version
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

def get_wikibio_predict_qg(data):       #里面很多名字没说全，可能漏掉了一个mid name，所有匹配上2/3即可
    all_predict = []
    for record in data:
        entity = record['entity'].split('(')[0].strip()     #去掉括号
        piece = entity.split(" ")
        answer = record['answer']       #直接取answer做字符串匹配，不要最后一步
        count_list = []
        for part in piece:
            if part.lower() in answer.lower():
                count_list.append(1)
            else:
                count_list.append(0)
        match_ratio = sum(count_list)/len(count_list)
        if entity.lower() in answer.lower() or match_ratio > 0.65:
            label = 'factual'
        else:
            label = 'non-factual'
        all_predict.append(label)
    
    return all_predict
  
 
'''use the following codes to calculate metrics on wikibio dataset'''

# data = read_data(wiki_bio_dataset) 
# ratio_list = get_wikibio_ratio(data)
# record = read_data(wikibio_em_record_path)
# predict_list = get_em_predict(record)
  

# map_predict = [label_mapping[i] for i in predict_list]
# acc = sum(map_predict)/len(map_predict)
# print(acc)
# predict_array = np.array(map_predict)
# ratio_array = np.array(ratio_list)
# new_array = predict_array * ratio_array
# print(new_array)
# print(sum(list(new_array))/sum(predict_array))

'''use the following codes to calculate metrics on PHD benchmark'''
data = read_data(data_path)
record = read_data(qg_record_path)
label_list = get_label(data)
predict_list = get_qg_predict(record)


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
