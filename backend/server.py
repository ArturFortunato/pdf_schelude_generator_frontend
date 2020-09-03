import flask
import flask_cors   
import json
from main import temp_main

app = flask.Flask(__name__)
app.config["DEBUG"] = True
flask_cors.CORS(app)


@app.route('/schedule', methods=['GET'])
def home():
    schedules = temp_main(['Inglês Vantagem Avançado (B2.2)', 'Cultura Clássica'])
    #Should receive a string with the courses comma separated
    print("This", flask.request.args.get('courses'))
    return schedules

app.run()