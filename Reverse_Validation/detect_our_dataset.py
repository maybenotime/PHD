from detection_components import *
from sklearn.metrics import f1_score
import json
from tqdm import tqdm



data_path = './process_annotated_data/data_store/verified_data_after_check.json'
qg_record_path = './our_dataset_qg_record.json'
em_record_path = './our_dataset_em_record.json'

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data

data = read_data(data_path)

all_record = []
for key,value in data.items():
    for entry in tqdm(value):
        result = question_generation_pipeline(entry['entity'],entry['AI'])
        all_record.append(result)

  
with open(qg_record_path,"w") as w:
    json.dump(all_record,w)
