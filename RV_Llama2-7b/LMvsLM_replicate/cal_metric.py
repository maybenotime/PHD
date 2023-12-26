from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score
import json
import numpy as np

verified_data_path = '/home/llama/inference/verified_data_after_check.json'
wiki_bio_dataset = './Self_check_gpt_data/new_wikibio_data.json' 
record_save_path = './lawyer_record.json'
wikibio_record_path = './wiki_bio_lawyer_record.json'

label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data


def read_record(path):          #存储出问题了，特殊处理一下
    data = []
    with open(path,"r") as f:
        str = f.read()
        split_str = str.split(']')
        for record in split_str[:300]:            
            full_record = record+']'
            record_list = json.loads(full_record)        #恢复成list
            data.append(record_list[-1]['content'])
    
    return data

def get_predict(data):
    pre_list = []
    for record_list in data:
        label_content = record_list[-1]['content']
        # print(label_content.lower())
        if 'correct' in label_content.lower() and 'incorrect' not in label_content.lower():
            label = 'factual'
        elif 'incorrect' in label_content.lower():
            label = 'non-factual'
        else:
            label = 'non-factual'
        pre_list.append(label)

    return pre_list

def get_label(data):
    all_label = []
    for key,value in data.items():
        for entry in value:
            all_label.append(entry['label'])
            
    return all_label

def get_wikibio_ratio(data):     #获得lable以及幻觉比例
    all_ratio = []
    for entry in data:
        all_ratio.append(entry['ratio'])
    
    return all_ratio

data = read_data(verified_data_path)
record = read_data(record_save_path)
label_list = get_label(data)
# ratio_list = get_wikibio_ratio(data)
predict_list = get_predict(record)

#计算wikibio dataset的代码
# map_predict = [label_mapping[i] for i in predict_list]

# print("acc:",sum(map_predict)/len(map_predict))

# predict_array = np.array(map_predict)
# ratio_array = np.array(ratio_list)
# new_array = predict_array * ratio_array
# print(sum(list(new_array))/sum(predict_array))

#下面是计算phd dataset的代码

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
