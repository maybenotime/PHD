from detection_components import *
import json
from collections import Counter
from tqdm import tqdm



wikibio_path = './LMvsLM_replicate/Self_check_gpt_data/new_wikibio_data.json'
qg_record_path = './wiki_bio_qg_record.json'
em_record_path = './wiki_bio_em_record.json'

label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data

data = read_data(wikibio_path)

all_record = []
for entry in tqdm(data):
    result = entity_matching_pipeline(entry['entity'],entry['gpt3_text'])
    all_record.append(result)

  
with open(em_record_path,"w") as w:
    json.dump(all_record,w)
