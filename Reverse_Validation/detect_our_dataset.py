#这是用我们的方法检测我们自己数据集的脚本
from detection_components import *
from sklearn.metrics import f1_score
import json
from tqdm import tqdm



data_path = './process_annotated_data/data_store/verified_data_after_check.json'
qa_record_path = './hal_detect_record/our_dataset_qa_record.json'
guess_record_path = './hal_detect_record/our_dataset_guess_record.json'
detail_record_path = './hal_detect_record/our_dataset_detail_record.json'

label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data

data = read_data(data_path)

predict_list= []           #预测结果
label_list = []
all_record = []
for key,value in data.items():
    for entry in tqdm(value):
        result = guess_entity_pipeline(entry['entity'],entry['AI'])
        predict = result['label']
        print(predict)
        label = entry['label']
        predict_list.append(predict)
        label_list.append(label)
        all_record.append(result)

map_label = [label_mapping[i] for i in label_list]
map_predict = [label_mapping[i] for i in predict_list]

f1 = f1_score(map_label, map_predict)
f1_1000w = f1_score(map_label[:100],map_predict[:100])
f1_10w = f1_score(map_label[100:200],map_predict[100:200])
f1_1y = f1_score(map_label[200:],map_predict[200:])
print(f1,f1_10w,f1_1000w,f1_1y)
  
with open(guess_record_path,"w") as w:
    json.dump(all_record,w)
