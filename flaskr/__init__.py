import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
    
    @app.route('/data')
    def data():
        int depression_rate
        int suicide_rate
        int student_to_depression_ratio

    @app.route('/colleges')
    def colleges(collegelist):
        str collegeID = ("")
        return "List of colleges is:" + collegelist

    @app.route('/investment')
    def investment():
        int investment_amount
        int planned_investment
        
    @app.route('/debt')
    def debt():
        int debt_amount
        int cost_of_living
    
        
