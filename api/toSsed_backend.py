from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello world", 200 # Code 200 means sucess


@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code s