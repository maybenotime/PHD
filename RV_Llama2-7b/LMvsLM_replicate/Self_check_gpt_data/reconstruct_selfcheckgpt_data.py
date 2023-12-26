import json

new_wikibio_dataset = 'new_wikibio_data.json'

with open("./dataset_v3.json", "r") as f:
    content = f.read()
dataset = json.loads(content)           #'gpt3_text'是幻觉文本  'gpt3_sentences' 分句结果  'annotation' 标注结果



def extract_entity(sentence):
    piece = sentence.split('(')
    name = piece[0].split(' ')
    if len(name) > 4:
        return None
    else:
        return piece[0]

def get_passage_label(annotation):
    score_map = {'major_inaccurate':1,'minor_inaccurate':1,'accurate':0}        #有幻觉就积一分，0分的就是完全没幻觉
    score_list = [int(score_map[label]) for label in annotation]
    sum_score = sum(score_list)
    hal_ratio = sum_score/len(score_list)       #幻觉比例
    return sum_score,hal_ratio
  
def reconstruct_dataset(dataset):          #提取出实体，把sentence_level标签转换为passage_level标签
    new_dataset = []
    for entry in dataset:
        entity = extract_entity(entry['gpt3_sentences'][0])
        if entity is not None:
            entry['entity'] = entity
            score,ratio = get_passage_label(entry['annotation'])
            if score == 0:
                entry['label'] = 'factual'
                entry['ratio'] = 0.0
            else:
                entry['label'] = 'non-factual'
                entry['ratio'] = round(ratio,1)
                new_dataset.append(entry)
    return new_dataset


new_dataset = reconstruct_dataset(dataset)

with open(new_wikibio_dataset,"w") as w:
    json.dump(new_dataset,w)
    
 
