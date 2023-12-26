import json
import time
import requests
from tqdm import tqdm
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score


our_dataset = './verified_data_after_check.json'
our_dataset_record = './zero-shot-baseline-record.json'

label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):
    with open(path,"r") as f:
        data = json.load(f)
    return data
        

def main_chat(entity,claim):
    instructs = "I want you to act as a claim judger. Given a claim about an entity, your objective is to determine if the provided claim contains non-factual\
 or hallucinated information. You should give your judgment based on world knowledge, only answer with factual or non-factual.\nEntity:{}\nClaim:{}"
    # instructs = 'Are you sure regarding the correctness of your claim? Please answer with Yes or No.\nClaim:{}'       #备用
    prompt = instructs.format(entity,claim)
    message =     [
        {"role": "user", "content": prompt},
    ]
    judgement = request_api(message)
    
    return judgement


def request_api(Prompts):          #把所有的api访问集中在一个函数
  flag = True
  while flag:
      try:
          result = requests.post(f"http://127.0.0.1:4396/",json={"message":Prompts})
          flag = False
      except Exception as e:
          print("try again!")
          print(e)
          time.sleep(5)
  text_response = result.text
  
  return text_response

def test_our_dataset(data):
    predict_list = []
    label_list= []
    for key,value in data.items():
        for entry in tqdm(value):
            judge = main_chat(entry['entity'],entry['AI'])
            print(judge)
            label = entry['label']
            if 'factual' in judge.lower():
                predict = 'factual'
            elif 'non-factual' in judge.lower():
                predict = 'non-factual'
            else:
                predict = 'non-factual'
            predict_list.append(predict)
            label_list.append(label)
    return predict_list,label_list

def test_wiki_bio(data):
    predict_list= []           #预测结果
    label_list = []
    for entry in tqdm(data):
        judge = main_chat(entry['entity'],entry['gpt3_text'])
        if 'factual' in judge.lower():
            predict = 'factual'
        else:
            predict = 'non-factual'
        print(predict)
        label = entry['label']
        predict_list.append(predict)
        label_list.append(label)
            
    return predict_list,label_list
    
def save_record(path,record):
    with open(path,"w") as w:
        json.dump(record,w)

    
data = read_data(our_dataset)
predict_list,label_list = test_our_dataset(data)
save_record(our_dataset_record,predict_list)

# data = read_data(wiki_bio_dataset)
# predict_list,label_list = test_wiki_bio(data)
# save_record(wiki_bio_record,predict_list)

map_label = [label_mapping[i] for i in label_list]
map_predict = [label_mapping[i] for i in predict_list]

# print(sum(map_predict)/len(map_predict))
# print("ACC:",accuracy_score(map_label,map_predict))

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
