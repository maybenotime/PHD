import json
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score

wiki_bio_score = './wiki_bio_score.json'
phd_benchmark_path = '/home/llama/inference/verified_data_after_check.json'
phd_benchmark_score = './phd_benchmark_score.json'

label_mapping = {'factual':0, 'non-factual':1}

def get_min_score(wiki_bio_score):
    with open(wiki_bio_score,"r") as f:
        data = json.load(f)
    min_score = min(data)
    return min_score

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

def predict(data,score):
    predict_list = []
    for value in data:
        if value > score:
            predict_list.append(1)
        else:
            predict_list.append(0)
    return predict_list
    
min_score = get_min_score(wiki_bio_score)
data = read_data(phd_benchmark_path)
phd_score = read_data(phd_benchmark_score)
label_list = get_label(data)
map_predict = predict(phd_score,min_score)



map_label = [label_mapping[i] for i in label_list]


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