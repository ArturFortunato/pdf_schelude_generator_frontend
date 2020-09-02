import flask
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/schedule', methods=['GET'])
def home():
    #Should receive a string with the courses comma separated
    print("This", flask.request.args.get('courses'))
    x = {'a': 3, 'b': 5}
    return x

app.run()