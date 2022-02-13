from tokenize import String
from flask import Flask
from flask import request
import redis
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

app = Flask(__name__)
firebase_admin.initialize_app(credentials.Certificate(json.loads(os.environ['key'])))
@app.route('/')
def hello_world():
    r = redis.Redis(
        host = os.environ['endpoint'],
        port = int(os.environ['port']),
        password = os.environ['password']
    )
    
    f = firestore.client()
    
    users_ref = f.collection(u'h4h')
    docs = users_ref.stream()
    
    try:
        id = request.args.get('id')
        data = r.get(id)
        data_json = json.loads(data)
        sum = 0
        n = 0

        for doc in docs:
            if(str(doc.get('id')) == id):
                sum+=doc.get('rating')
                n+=1
                
        try:
            data_json['user_rating'] = sum/n
        except:
            data_json['user_rating'] = 5
        
        return data_json
    
    except:
        error_result = {"name":"ERROR","location":"ERROR, CA","depression_stats_percent":0.10,"depression_stats":10,"student_to_mh_ratio_percent":0.69,"student_to_mh_ratio":69,"investment_into_mh_percent":0.30,"investment_into_mh":30,"cost_of_living_and_debt_percent":0.40,"cost_of_living_and_debt":40,"suicide_rate_percent":1.0,"suicide_rate":100}
        return json.dumps(error_result)

@app.route('/ratings')
def ratings():
    f = firestore.client()
    
    users_ref = f.collection(u'h4h')
    docs = users_ref.stream()

    try:
        id = request.args.get('id')
    except:
        id = 1

    sum = 0
    n = 0

    for doc in docs:
        if(str(doc.get('id')) == id):
            sum+=doc.get('rating')
            n+=1
            
    try:
        return str(sum/n)
    except:
        return "3.5"