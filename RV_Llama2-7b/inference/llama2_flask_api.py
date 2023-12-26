import torch
import os
import sys
import warnings
from typing import List

from flask import Flask, jsonify, request
from gevent import pywsgi
import json

from transformers import LlamaConfig, LlamaTokenizer, LlamaForCausalLM, AutoTokenizer
from model_utils import load_model
from chat_utils import read_dialogs_from_file, format_api_chat


seed = 42
model_path = '/hy-tmp/Llama-2-7b-chat-hf'


print('ready to predict')
app = Flask(__name__)

torch.cuda.manual_seed(seed)
torch.manual_seed(seed)
model = load_model(model_path,True)     #量化
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.add_special_tokens(
    {
        
        "pad_token": "<PAD>",
    }
)

@app.route(f"/", methods=['get', 'post'])
def api():
    message_json = request.json.get('message')
    chat = format_api_chat(message_json,tokenizer)
    response = complete_chat(chat,message_json)
   
    return response


def complete_chat(chat,dialog_history):
    with torch.no_grad():
        tokens= torch.tensor(chat).long()
        tokens= tokens.unsqueeze(0)
        tokens= tokens.to("cuda:0")
        outputs = model.generate(
            tokens,
            max_new_tokens=256,
            do_sample=True,
            top_p=0.05,
            temperature=0.1,
            use_cache=True,
            top_k=1,
            repetition_penalty=1.0,
            length_penalty=1,
        )
        output_text = tokenizer.decode(outputs[0, len(tokens[0]):-1], skip_special_tokens=True)

    return output_text
    


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 10043), app)
    server.serve_forever()