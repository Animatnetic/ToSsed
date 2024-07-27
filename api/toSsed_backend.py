import os
from ai71 import AI71
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv() # Initializing dot environment variables
API_KEY = os.getenv("AI71_API_KEY")
model_name = "tiiuae/falcon-180B-chat"

app = Flask(__name__)
client = AI71(API_KEY)


@app.route("/summarize")
def home():
    result = client.chat.completions.create(
        model=model_name, 
        messages=[
            {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair"},
            {"role": "user", "content": "Hello, what are you?"}
        ]
    )
    print(result)

    return result


@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code
