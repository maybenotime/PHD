import json

stage2_result = './RV_result/stage2_result_v2.json'
data_path = './verified_data_after_check.json'
record_path = './RV_result/RV_em_result_v2.json'

def read_data(path):            
    with open(path,"r") as f:
        data = json.load(f)
    return data

def save_data(data,path):    #json
    with open(path,"w") as w:
        json.dump(data,w)

def entity_list():
    entity_list = []
    data = read_data(data_path)
    for key,value in data.items():
        for entry in value:
            entity = entry['entity']
            entity_list.append(entity)
    return entity_list

def write_record(entity_list):
    record_list = []
    answer_list = read_data(stage2_result)
    for entity,answer in zip(entity_list,answer_list):
        record = {}
        record['entity'] = entity
        record['answer'] = answer
        record_list.append(record)
    save_data(record_list,record_path)

write_record(entity_list())
    


