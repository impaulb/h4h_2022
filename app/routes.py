from app import app
from flask import request
import redis
import json
import os

@app.route("/data")
def index():
    
    file = open("env.txt","r")
    env_vars = file.readlines()
    
    r = redis.Redis(
        host = env_vars[0][:-1],
        port = int(env_vars[1][:-1]),
        password = env_vars[2]
    )
    
    file.close()
    
    try:
        id = request.args.get('id')
        data = r.get(id)
        data_json = json.loads(data)
        return data_json
    except:
        error_result = {'depression_stats':99999,"student_to_mh_ratio":99999, "investment_into_mh":99999,"cost_of_living_and_debt":99999,"suicide_rate":99999}
        return json.dumps(error_result)