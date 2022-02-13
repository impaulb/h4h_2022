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
    
    try:
        id = request.args.get('id')
        data = r.get(id)
        data_json = json.loads(data)
        return data_json
    except:
        error_result = {'depression_stats':99999,"student_to_mh_ratio":99999, "investment_into_mh":99999,"cost_of_living_and_debt":99999,"suicide_rate":99999}
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