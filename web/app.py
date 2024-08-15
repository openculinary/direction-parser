from flask import Flask, jsonify, request
import httpx


app = Flask(__name__)


@app.route("/", methods=["POST"])
def root():
    _ = request.form.get("language_code", type=str, default="en")
    descriptions = request.form.getlist("descriptions[]")
    equipment_data = httpx.post(
        url="http://knowledge-graph-service/directions/query",
        data={"descriptions[]": descriptions},
        proxy=None,
    )
    return jsonify(equipment_data.json())
