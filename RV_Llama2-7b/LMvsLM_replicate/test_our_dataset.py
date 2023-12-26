from LM_vs_LM import *
import json
from tqdm import tqdm
from collections import Counter


data_path = '/home/llama/inference/verified_data_after_check.json'
wikibio_path = './Self_check_gpt_data/new_wikibio_data.json'        #这是筛选后的全错的数据集
record_save_path = './lawyer_record.json'

label_mapping = {'factual':0, 'non-factual':1}

def read_data(path):             #读取数据集
    with open(path,"r") as f:
        data = json.load(f)
    return data


def detect_hal(entity,claim):
    lawyer = exmainer(claim)
    suspect = Suspect(entity, claim)
    question = lawyer.Setup()       #提问
    trigger = True      #是否继续询问
    count = 1           #询问轮次计数
    while(trigger):
        count += 1
        answer = suspect.answer_without_history(question)  #回答
        flag = lawyer.check_follow_up_question(answer) #是否继续提问？
        if 'next question' not in flag or count == 3:                #不问了，直接出结论
            lawyer_history = lawyer.decision()
            trigger = False             #退出询问
        else:                           #继续问
            # question = lawyer.ask_continue()                                  #llama的回答格式有些不同
            continue
            
    return lawyer_history[-1]['content'],lawyer_history

#这一段是检测our_data
data = read_data(data_path)
all_history = []
all_label = []
all_gt = []
for key,value in data.items():
    for entry in tqdm(value):
        ground_truth = entry['label']
        label_content,history = detect_hal(entry['entity'],entry['AI'])
        if 'correct' in label_content.lower() and 'incorrect' not in label_content.lower():
            label = 'factual'
        elif 'incorrect' in label_content.lower():
            label = 'non-factual'
        else:
            label = 'non-factual'
        print(label)
        print(history)
        all_history.append(history)
        all_label.append(label) 
        all_gt.append(ground_truth)

with open(record_save_path,'w') as w:
    json.dump(all_history,w)




map_label = [label_mapping[i] for i in all_gt]
map_predict = [label_mapping[i] for i in all_label]

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




#这一段是检测wikibio dataset
# data = read_data(wikibio_path)
# all_label= []           #存储label
# all_history = []
# for entry in data:
#         label_content,history = detect_hal(entry['entity'],entry['gpt3_text'])
#         print(history)
#         if 'correct' in label_content.lower() and 'incorrect' not in label_content.lower():
#             label = 'factual'
#         elif 'incorrect' in label_content.lower():
#             label = 'non-factual'
#         else:
#             label = 'non-factual'
            
#         print(label)
#         all_label.append(label)
#         all_history.append(history)

# acc = Counter(all_label)
# print(acc)

# with open(record_save_path,'w') as w:
#     json.dump(all_history,w)
    
