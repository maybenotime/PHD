import spacy
import json
nlp = spacy.load("en_core_web_sm")

data_path = './sampled_phd_benchmark.json'

def read_data(path):
    with open(path,"r") as f:
       data =  json.load(f)
       return data
    
def split_sentence(data):
    new_data = []
    for entry in data:
        passage = entry['AI']
        sentences = [str(sent) for sent in nlp(passage).sents]
        entry['sentences'] = sentences
        new_data.append(entry)
        
    return new_data

def save_new_data(path,new_data):
    with open(path,"w") as w:
        json.dump(new_data,w)

data = read_data(data_path)
new_data = split_sentence(data)
save_new_data(data_path,new_data)