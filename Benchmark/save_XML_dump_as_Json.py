#转储为json格式
from bs4 import BeautifulSoup
import re
import json

wiki_path = './enwiki-20210820-abstract.xml'  #this file is too large, please load from this link: https://archive.org/download/enwiki-20210820
save_path = './enwiki_entity_20210820.json'   #After you download the above file, you can run this script to get a json type dump file  

with open(wiki_path,"r") as f, open(save_path,"w") as w:
    for line in f:
        soup = BeautifulSoup(line, "html.parser")
        if soup.find('title'):
            str = soup.find('title')
            title = re.findall(r"Wikipedia:\s(.+)",str.text)
            entity = {}             #新建实体
            entity['title'] = title[0]
        elif soup.find('url'):
            url = soup.find('url')
            entity['url'] = url.text
        elif soup.find('abstract'):
            abstract = soup.find('abstract')
            entity['abstract'] = abstract.text
            entity_json = json.dumps(entity)
            print(entity_json,file=w)