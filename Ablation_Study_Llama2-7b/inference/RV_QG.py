from chat_completion import main
import fire
import json
import re

data_path = './verified_data_after_check.json'
stage1_prompt = './RV_QA/stage1_prompt.json'
stage1_result = './RV_QA/stage1_result.json'
stage2_prompt = './RV_QA/stage2_prompt.json'
stage2_result = './RV_QA/stage2_result.json'

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
            prompts = "I will give you some information about the entity. You should use all this information to generate a question, and the answer to your question is the entity. Do not include the entity in your question.\
  \nentity:World War II\ninformation: World War II, also known as the Second World War, was a global war that lasted from 1939 to 1945.\nquestion: which global war lasted from 1939 to 1945?\n\
entity: {}\ninformation: {}\n Now, give the question only."
            prompts = prompts.format(entity,content)
            temple_list = [{"role": "user", "content": prompts}]
            prompt_list.append(temple_list)
    return prompt_list


def perform_stage1():
    result = main(prompt_file=stage1_prompt)
    save_data(result,stage1_result)
    return result


def prepare_stage2_data(question_list):
    prompt_list = []
    for question in question_list:
        prompts = 'You should answer the following question as short as possible. {}'
        prompts = prompts.format(question)
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
    # stage2_data = prepare_stage2_data(result)
    # save_data(stage2_data,stage2_prompt)
    result = perform_stage2()
    print(result)
