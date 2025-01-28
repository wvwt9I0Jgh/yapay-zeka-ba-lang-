from flask import Flask, render_template, request, jsonify # type: ignore

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    response = "Bu, aldığınız mesajın yanıtıdır: " + message
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
import random

# Gerekli NLTK veri dosyalarını indir
nltk.download('punkt')

app = Flask(__name__)

class DanteAI:
    def __init__(self):
        self.name = "Dante"
        self.model_path = os.path.join(
            os.path.expanduser("~/Desktop/yapay_zeka"),
            "dante_brain.json"
        )
        self.load_or_create_memory()
        self.load_basic_responses()
    
    def load_or_create_memory(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'r', encoding='utf-8') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                'conversations': [],
                'learned_responses': {},
                'data_analysis': {}
            }
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            self.save_memory()

    def load_basic_responses(self):
        self.basic_responses = {
            'greeting': ['Merhaba!', 'Selam!', 'Hey, nasılsın?'],
            'farewell': ['Görüşürüz!', 'Hoşça kal!', 'İyi günler!'],
            'unknown': ['Bunu henüz bilmiyorum. Bana öğretir misin?',
                       'Bu konu hakkında daha fazla bilgi verebilir misin?',
                       'Bunu anlamadım. Biraz daha açıklar mısın?'],
            'thanks': ['Rica ederim!', 'Ne demek!', 'Önemli değil!']
        }

    def process_message(self, message):
        if not message.strip():
            return "Bir mesaj yazmalısın!"
        
        tokens = word_tokenize(message.lower())
        
        if any(word in tokens for word in ['merhaba', 'selam', 'hey']):
            return random.choice(self.basic_responses['greeting'])
        elif any(word in tokens for word in ['güle', 'hoşça', 'görüşürüz']):
            return random.choice(self.basic_responses['farewell'])
        elif any(word in tokens for word in ['teşekkür', 'sağol', 'eyvallah']):
            return random.choice(self.basic_responses['thanks'])
            
        return random.choice(self.basic_responses['unknown'])

    def save_memory(self):
        with open(self.model_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=4)

dante = DanteAI()

@app.route('/')
def home():
    return render_template('sohbet.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    response = dante.process_message(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)