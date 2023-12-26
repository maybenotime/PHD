#这个数据集里直接有采样结果，可以直接用
from selfcheckgpt.modeling_selfcheck import SelfCheckBERTScore
import json
import torch
import time
from tqdm import tqdm
from collections import Counter

torch.manual_seed(28)

data_path = './sampled_phd_backup.json'
save_score_path = './phd_benchmark_score.json'


label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data

data = read_data(data_path)
selfcheck_bertscore = SelfCheckBERTScore()

all_score = []
for entry in tqdm(data):
    while True:
        try:
            sen_scores_bertscore = selfcheck_bertscore.predict(
                sentences= entry['sentences'],
                sampled_passages= entry['samples_text']            #由于计算时间原因,只采样三条
            )
            break
        except Exception as e:
            print("try again")
            time.sleep(3)
            
    passage_score = sum(sen_scores_bertscore)/len(sen_scores_bertscore)         #大于0.5即为幻觉
    print(float(passage_score))
    all_score.append(float(passage_score))
    
    
min_score = min(all_score)
print(min_score)

with open(save_score_path,"w") as w:
    json.dump(all_score,w)

    