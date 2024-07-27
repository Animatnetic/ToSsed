import os
import ai71
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv() # Initializing dot environment variables
api_key = os.getenv("AI71_API_KEY")


app = Flask(__name__)


@app.route("/summarize")
def home():
    return jsonify({"status": 200, "message": "This is a test for the GET request"}), 200


@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code
