#附上各实体的搜索结果数
import json 
from request_google import google_research


save_path = './enwiki_entity_20210820.json'
final_path = './enwiki_entity_plus_num_20210820.json'

#entry有title,url,abstract 三个属性
with open(save_path,"r") as f, open(final_path,"a") as w:
    flag = False    #未到存档点不开始research
    for line in f:
        entry = json.loads(line)
        entity = entry['title']
        if entity == '147 BC':          #修改存档点
            flag = True
            continue
        if flag is True:
            try:
                num = google_research().get_num_of_result(entity,sleep=3)
                entry['num'] = num
                print(entry)
                entry_json = json.dumps(entry)
                print(entry_json,file=w)
            except Exception as e:
                print(e)
        else:
            continue