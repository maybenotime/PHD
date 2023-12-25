from LM_vs_LM import *
import json
from tqdm import tqdm
from collections import Counter

data_path = '../process_annotated_data/data_store/verified_data_after_check.json'   #PHD benchmark
wikibio_path = './Self_check_gpt_data/new_wikibio_data.json'        #这是筛选后的数据集
record_save_path = './lawyer_record.json'



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
        if 'No' in flag or count == 5:                #控制轮次
            lawyer_history = lawyer.decision()
            trigger = False             #退出询问
        else:                           #继续问
            question = lawyer.ask_continue()
            
    return lawyer_history[-1]['content'],lawyer_history

#这一段是检测our_data
data = read_data(data_path)
all_history = []
for key,value in data.items():
    all_label = []
    for entry in tqdm(value):
        label_content,history = detect_hal(entry['entity'],entry['AI'])
        if 'correct' in label_content.lower() and 'incorrect' not in label_content.lower():
            label = 'factual'
        elif 'incorrect' in label_content.lower():
            label = 'non-factual'
        else:
            label = 'non-factual'
        print(label)
        all_history.append(history) 

with open(record_save_path,'w') as w:
    json.dump(all_history,w)


'''use the following codes to detect wikibio dataset'''
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
    
