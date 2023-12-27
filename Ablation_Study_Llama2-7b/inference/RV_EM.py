from chat_completion import main
import fire
import json
import re

data_path = './verified_data_after_check.json'
stage1_prompt = './RV_result/stage1_prompt.json'
stage1_result = './RV_result/stage1_result.json'
stage2_prompt = './RV_result/stage2_prompt.json'
stage2_result = './RV_result/stage2_result.json'

def read_data(path):            
    with open(path,"r") as f:
        data = json.load(f)
    return data

def save_data(data,path):    #json
    with open(path,"w") as w:
        json.dump(data,w)

def prepare_stage1_data():
    prompt_list = []
    data = read_data(data_path)
    print(data["wiki_1000w"][0].keys())
    for key,value in data.items():
        for entry in value:
            content = entry['AI']
            entity = entry['entity']
            prompts = '{} Please list all features of {} which mentioned in above passage with number, do not include {} in your list.'
            prompts = prompts.format(content,entity,entity)
            temple_list = [{"role": "user", "content": prompts}]
            prompt_list.append(temple_list)
    return prompt_list


def perform_stage1():
    result = main(prompt_file=stage1_prompt)
    save_data(result,stage1_result)
    return result

def post_process_answer(result_list):      #该函数用于处理标签泄露
    detail_list = []
    for detail in result_list:
        temple_list = re.findall(r'(\d\.[^\d]+)\n',detail)
        detail_str = '\n'.join(temple_list)
        detail_list.append(detail_str)
    return detail_list


def prepare_stage2_data(result_list):
    detail_list = post_process_answer(result_list)
    prompt_list = []
    for detail in detail_list:
        prompts = 'You should find an entity conform to the following describtion: {}. If you fail to find a perfect match, please say an entity that mathes the requirements as much as possible. You need to give the percentage of the entity that meets requirements.'
        prompts = prompts.format(detail)
        temple_list = [{"role": "user", "content": prompts}]
        prompt_list.append(temple_list)
    return prompt_list

def perform_stage2():
    result = main(prompt_file=stage2_prompt)
    save_data(result,stage2_result)
    return result

if __name__ == "__main__":
    # data = prepare_stage1_data()
    # save_data(data,stage1_prompt)
    # result = perform_stage1()
    result = read_data(stage1_result)
    stage2_data = prepare_stage2_data(result)
    save_data(stage2_data,stage2_prompt)
    res = perform_stage2()
    print(res)
