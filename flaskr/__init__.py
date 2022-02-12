import os
from os import environ
from tokenize import String
from flask import Flask
from flask import request
import redis
import json

def create_app(test_config=None):
    # create and configure the app'
    app = Flask(__name__, instance_relative_config=True)
    
    file = open("env.txt","r").readlines()
    
    r = redis.Redis(
        host = file[0][:-1],
        port = int(file[1][:-1]),
        password = file[2]
    )
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/data')
    def data():
        try:
            id = request.args.get('id')
            data = r.get(id)
            data_json = json.loads(data)
            return data_json
        except:
            error_result = {'depression_stats':99999,"student_to_mh_ratio":99999, "investment_into_mh":99999,"cost_of_living_and_debt":99999,"suicide_rate":99999}
            return json.dumps(error_result)
        
    return app
