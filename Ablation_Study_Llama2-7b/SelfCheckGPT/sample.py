import json
import time
import requests
from tqdm import tqdm


data_path = '/home/llama/inference/verified_data_after_check.json'
save_path = './sampled_phd.json'


def samples(entity):
    sample_list = []        #存储sample的结果
    sys_prompt = "Answer the following question only if you know the answer or can make a well-informed guess; otherwise tell me you don't know it"
    instructs = "Please write a brief Wikipedia for {} under 100 words."     
    prompt = instructs.format(entity)
    message = [{"role": "system", "content":sys_prompt},{"role": "user", "content":prompt}]
    for i in range(3):
        sample = request_api(message)
        sample_list.append(sample)
    return sample_list

def request_api(message):
    flag = True
    while flag:
        try:
            result = requests.post(f"http://127.0.0.1:10043/",json={"message":message})
            flag = False
        except Exception:
            print("try again!")
            time.sleep(5)
            
    text_response = result.text
    return text_response

def read_data(path):
    with open(path,"r") as f:
        data = json.load(f)
    return data

def add_samples_to_data(data):
    new_data = []
    for key,value in data.items():
        for entry in tqdm(value):
            sample_list = samples(entry['entity'])
            entry['samples_text'] = sample_list
            new_data.append(entry)
    return new_data
    
def save_new_data(path,new_data):
    with open(path,"w") as w:
        json.dump(new_data,w)

data = read_data(data_path)
new_data = add_samples_to_data(data)
save_new_data(save_path,new_data)