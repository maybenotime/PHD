#access google to get result
import requests
from bs4 import BeautifulSoup
import time
import random
import cchardet

domain_path = './all_domain.txt'
agent_path = './all_agent.txt'
URL = "https://{domain}/search?hl={language}&q={query}"


#防止封IP trick    1.随机睡眠  2.谷歌域名轮询   3.ip轮询
class google_research():
    def __init__(self):
        self.domain_list = self.get_domain_list(domain_path)
        self.agent_list = self.get_agent_list(agent_path)
        
    def get_num_of_result(self,entity,language='en',sleep=10):
        sleep_time = random.randint(sleep-2,sleep+2)      
        time.sleep(sleep)               #随机休眠
        domain = random.choice(self.domain_list)
        query = self.space_to_plus(entity)
        url = URL.format(domain=domain,language=language,query=query) #域名轮询
        print(url)
        user_agent = random.choice(self.agent_list) #随机user_agent
        print(user_agent)
        headers = {"user-agent" : user_agent,'Connection':'close'}
        re = requests.get(url,allow_redirects=False,verify=False,timeout=10,headers=headers)
        soup = BeautifulSoup(re.content, "html.parser")
        result_dev = soup.find('div', {'id': 'result-stats'})
        return int(result_dev.text.replace(',', '').split()[1])

    def get_domain_list(self,path):
        domain_list = []
        with open(path,"r") as f:
            for line in f:
                line = line.strip()
                domain_list.append(line)
        return domain_list
    
    def get_agent_list(self,path):
        agent_list = []
        with open(path,"r") as f:
            for line in f:
                line = line.strip()
                agent_list.append(line)
        return agent_list

    def space_to_plus(self,entity):        #空格替换为加号
        query = entity.replace(" ","+")
        return query
