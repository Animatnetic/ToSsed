import os
from ai71 import AI71
from flask import Flask, jsonify
from dotenv import load_dotenv
import requests

load_dotenv() # Initializing dot environment variables
API_KEY = os.getenv("AI71_API_KEY")
API_URL = "https://api.ai71.ai/v1/chat/completions"

app = Flask(__name__)
model_name = "tiiuae/falcon-180b-chat"
client = AI71(AI71_API_KEY)

@app.route("/summarize")
def home():
    result = []

    for outputChunk in client.chat.completions.create(
        model=model_name, 
        messages=[
            {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair"},
            {"role": "user", "content": "Hello, what are you?"}
        ], 
        stream=True
    ):
        if outputChunk.choices[0].delta.content:
            result.append(outputChunk.choices[0].delta.content)
    
    result = "".join(result) # Parse array of results into a single string

    return jsonify({"result": result}), 200


@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code


if __name__ == "__main__":
    app.run()
