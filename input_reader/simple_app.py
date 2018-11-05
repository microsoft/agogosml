from flask import Flask, request
import requests
import code
import transformer
import json

app = Flask(__name__)

#data = {"intValue": 50, "floatValue": 3.5, "timeValue": "time!", "boolValue": "false", "stringValue": "tweety"}
#requests.post("http://localhost:5000/input", data=json.dumps(data))
@app.route("/input", methods=["POST"])
def input():
    result = request.get_json(force=True)
    transformed_result = transformer.transform(result)
    serialized_result = json.dumps(transformed_result)
    requests.post("http://localhost:5000/output", data=serialized_result)
    return serialized_result

@app.route("/output", methods=["POST"])
def output():
    result = request.get_json(force=True)
    print(result)
    return result

app.run(debug=True)
