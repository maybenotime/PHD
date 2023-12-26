import json
import re

final_path = './enwiki_entity_plus_num_20210820.json'
under_10w = './under10w_entity.json'            
domain_1000w = './domain1000w_entity.json'
above_1y = './above1y_entity.json'

splited_data = {}
with open(final_path,"r") as f:
    for line in f:
        entry = json.loads(line)
        entity = entry['title']
        if len(re.findall("(\d)+(s)?\sBC",entity)) != 0:         #删去指代不明确的年份实体
            continue
        if re.fullmatch("(\d)+",entity) is not None:         #删去指代不明确的年份实体
            continue
        num = entry['num']
        if num < 100000:
            if '10w' not in splited_data:
                splited_data['10w'] = []
                splited_data['10w'].append(entry)
            else:
                splited_data['10w'].append(entry)
        elif 100000 <= num < 1000000:
            if '100w' not in splited_data:
                splited_data['100w'] = []
                splited_data['100w'].append(entry)
            else:
                splited_data['100w'].append(entry)
        elif 1000000 <= num < 10000000:
            if '1kw' not in splited_data:
                splited_data['1kw'] = []
                splited_data['1kw'].append(entry)
            else:
                splited_data['1kw'].append(entry)
        elif 10000000 <= num < 100000000:
            if '10kw' not in splited_data:
                splited_data['10kw'] = []
                splited_data['10kw'].append(entry)
            else:
                splited_data['10kw'].append(entry)
        elif 100000000 <= num :      #大于1亿
            if 'inf' not in splited_data:
                splited_data['inf'] = []
                splited_data['inf'].append(entry)
            else:
                splited_data['inf'].append(entry)
    

for key,list in splited_data.items():
    print(key,len(list)) 

with open(under_10w,"w") as w:
    json.dump(splited_data['10w'],w)
    
with open(domain_1000w,"w") as w:
    json.dump(splited_data['1kw'],w)
         
with open(above_1y,"w") as w:
    json.dump(splited_data['inf'],w)                              
    
