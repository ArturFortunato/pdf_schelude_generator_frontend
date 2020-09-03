import flask
import flask_cors   
import json
from main import main

app = flask.Flask(__name__)
app.config["DEBUG"] = True
flask_cors.CORS(app)


@app.route('/schedule', methods=['GET'])
def home():
    print(main())
    #Should receive a string with the courses comma separated
    print("This", flask.request.args.get('courses'))
    x = {0: [
                {
                    'name': 'test',
                    'start': '2020-09-04 10:00:00',
                    'end': '2020-09-04 11:30:00',
                    'color': 'red',
                },
            ]
    }
    return json.dumps(x)

app.run()