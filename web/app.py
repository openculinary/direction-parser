from flask import Flask, jsonify, request
import requests


app = Flask(__name__)


@app.route("/", methods=["POST"])
def root():
    descriptions = request.form.getlist("descriptions[]")
    equipment_data = requests.post(
        url="http://knowledge-graph-service/directions/query",
        data={"descriptions[]": descriptions},
        proxies={},
    )
    return jsonify(equipment_data.json())
