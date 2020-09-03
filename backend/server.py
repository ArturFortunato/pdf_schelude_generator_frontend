import flask
import flask_cors   
import json
from main import temp_main

app = flask.Flask(__name__)
app.config["DEBUG"] = True
flask_cors.CORS(app)


@app.route('/schedule', methods=['POST'])
def home():
    schedules = temp_main(flask.request.get_json()['courses'])
    return schedules

app.run()