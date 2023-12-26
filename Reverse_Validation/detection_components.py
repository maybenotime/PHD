import openai
import time
import re

openai.api_key = ''



def main_chat(entity):       #use this function to generate wikipedia
  sys_prompt = "Answer the following question only if you know the answer or can make a well-informed guess; otherwise tell me you don't know it"
  instructs = "Please write a brief Wikipedia for {} under 100 words."    
  prompt = instructs.format(entity)
  
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": prompt}],
      max_tokens=256,
      temperature=0           
      )
  text_response = response["choices"][0]["message"]["content"]
  return text_response


def question_generation(entity,content):
  instructs = "I will give you some information about the entity. You should use all this information to generate a question, and the answer to your question is the entity. Do not include the entity in your question.\
  \nThere is an example.\nentity:World War II\ninformation: World War II, also known as the Second World War, was a global war that lasted from 1939 to 1945.\nquestion: which global war lasted from 1939 to 1945?\n\
  entity: {}\ninformation: {}\nquestion:"     
  prompt = instructs.format(entity,content)
  response = request_api(prompt)
  return response
      
def reverse_modeling(question):
  prompt = "You should answer the following question as short as possible. {}"     #一个系统级的prompt，用于指定chatgpt的人格
  prompt = prompt.format(question)
  response = request_api(prompt)
  return response 

def list_detail(entity,content):  #将实体的信息一条条列出
  prompts = '{} Please list all features of {} which mentioned in above with number, do not include {} in your list.'
  prompts = prompts.format(content,entity,entity)
  response = request_api(prompts)
  return response 

def entity_conform_to_detail(detail):   #猜测最符合信息的实体，并汇报符合的总条数。   比如 entity: XXX  Acc: 6/7                           
  prompts = 'You should find an entity conform to the following describtion: {}. If you fail to find a perfect match, please say an entity that mathes the requirements as much as possible. You need to give the percentage of the entity that meets requirements.'
  prompts = prompts.format(detail)
  response = request_api(prompts)
  return response 

def ask_if_not_same(entity,detail):      #如果没找到最符合（百分百）的实体，就直接问答案是否符合,这个用来做Baseline吧
  prompts = 'Can {} conform to the following describtion? {} You need to give the percentage of the entity that meets requirements.'
  prompts =prompts.format(entity,detail)
  response = request_api(prompts)
  return response
  
def guess_entity(question):       #让模型猜测被MASK的实体
  instruction = "I will provide a description of an entity where the name of the entity is masked with the [mask] symbol,\
now I need you to guess the entity based on the remaining information.\nThere is an example.\ndescription: [mask], also known as the Second World War, was a global war that lasted from 1939 to 1945.\
\nThe entity masked by [mask] is: World War II.\ndescription: {}\nThe entity masked by [mask] is:"
  prompt = instruction.format(question)
  response = request_api(prompt)
  return response

def is_same_entity(entity,answer):       #判断是否是同一个实体，考虑到别名等情况,但并不是特别靠谱，优先字符串匹配
  prompts = '{} Please identify whether above entity refer to same with {}, only answer Yes or No.'
  response = request_api(prompts.format(answer,entity))
  return response

def request_api(Prompts):          #把所有的api访问集中在一个函数
  flag = True
  while flag:
      try:
          response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[{"role": "user", "content": Prompts}],
              max_tokens=256,
              temperature=0           
            )
          flag = False
      except Exception as e:
          print("try again!")
          print(e)
          time.sleep(5)
  text_response = response["choices"][0]["message"]["content"]
  cost = response["usage"]["total_tokens"]


  return text_response

  

def question_generation_pipeline(entity, content):      #输入entity以及模型生成的content,通过question generation来反向建模
  # content = main_chat(entity)       #生成关于entity的content
  question = question_generation(entity,content)    #生成关于content的question
  answer = reverse_modeling(question)   #得到答案
  #应该还有一步判断entity和answer是否是一个东西，也可以采用NLI
  result = 'None'       #表示没到is_same_entity这一步  
  if entity.strip().lower() in answer.lower():    #这一步应当是优先判断
    label = 'factual'
  else:
    result = is_same_entity(entity,answer)    #yes不一定靠谱，对蕴含关系可能存在误判，但NO是比较靠谱的
    if 'No' in result:
      label = 'non-factual'
    if 'Yes' in result:
      label = 'factual'            
    else:                          #特殊情况
      label = 'non-factual'
  
  record = {'entity':entity,'claim':content,'question':question,'answer':answer,'Is_same':result, 'label':label}  
  
  return record



def guess_entity_pipeline(entity,content):      #通过将实体信息掩盖，让模型猜测来实现反向建模
  mask_content = content.replace(entity,"[mask]")      #替换为[mask] 标记
  answer = guess_entity(mask_content)
  result = 'None'       #表示没到is_same_entity这一步
  if entity.strip().lower() in answer.lower():    #这一步应当是优先判断
    label = 'factual'
  else:
    result = is_same_entity(entity,answer)    #yes不一定靠谱，对蕴含关系可能存在误判，但NO是比较靠谱的
    # print(result)
    if 'No' in result:
      label = 'non-factual'
    if 'Yes' in result:
      label = 'factual'            
    else:                          #这种情况是模型压根没猜东西
      label = 'non-factual'
  
  record = {'entity':entity,'claim':content,'answer':answer,'Is_same':result, 'label':label}  
  return record

def detect_in_sentence_level_pipeline(entity,content):      #这个函数是RV-EM
    detail = list_detail(entity,content)
    answer = entity_conform_to_detail(detail)
    result = 'None'       #表示没到is_same_entity这一步  
    if '100%' in answer:    #要百分百符合要求,否则就是幻觉
      if entity.strip().lower() in answer.lower():    #猜对的同时
        label = 'factual'
      else:
        result = is_same_entity(entity,answer)    #yes不一定靠谱，对蕴含关系可能存在误判，但NO是比较靠谱的
        if 'No' in result:
          label = 'non-factual'
        elif 'Yes' in result:
          label = 'factual'            #待人工核验，但可以直接作为factual 处理
        else:
          label = 'non-factual'           
    else:
      label = 'non-factual'
    
    record = {'entity':entity,'claim':content,'detail':detail,'answer':answer,'Is_same':result,'label':label} 
    return record
  

  
if __name__ == '__main__':
  record = question_generation_pipeline('Proclamation 10043')
  
