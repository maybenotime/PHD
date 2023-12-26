from detection_components import *
from sklearn.metrics import f1_score
import json
from collections import Counter
from tqdm import tqdm



wikibio_path = './LMvsLM_replicate/Self_check_gpt_data/new_wikibio_data.json'
qa_record_path = './hal_detect_record/wiki_bio_qa_record.json'
guess_record_path = './hal_detect_record/wiki_bio_guess_record.json'
detail_record_path = './hal_detect_record/wiki_bio_detail_record.json'

label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data

data = read_data(wikibio_path)

predict_list= []           #预测结果
label_list = []
all_record = []
for entry in tqdm(data):
    result = detect_in_sentence_level_pipeline(entry['entity'],entry['gpt3_text'])
    predict = result['label']
    print(predict)
    label = entry['label']
    predict_list.append(predict)
    label_list.append(label)
    all_record.append(result)

acc = Counter(predict_list)
print(acc)
  
with open(detail_record_path,"w") as w:
    json.dump(all_record,w)
