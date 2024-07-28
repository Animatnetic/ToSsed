import os
from ai71 import AI71
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv() # Initializing dot environment variables
API_KEY = os.environ.get("AI71_API_KEY")
API_URL = "https://api.ai71.ai/v1/chat/completions"

app = Flask(__name__)
model_name = "tiiuae/falcon-180b-chat"
client = AI71(API_KEY)


@app.route("/summarize", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        text_input = request.args.get("input")

        all_results = {}

        if text_input == "" or text_input is None:
            return jsonify({"result": None}), 200 # Returning nothing has to not waste tokens/computation on empty inputs.
        else:
            max_chunk_size = 1500 # Tokens, in this case of which is "characters"
            chunks = [text_input[i: i+max_chunk_size] for i in range(0, len(text_input), max_chunk_size)] # Breaks up the input into chunks of 1500 characters intervals to operate them individually


            for chunk_index, chunk in enumerate(chunks):
                result_chunk = client.chat.completions.create(
                    model=model_name, 
                    messages=[
                        {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair. Along side this, you will grade the inputted ToS via the grading system a website called 'ToS; DR' uses. You only return data in JSON format with the value within the key value pair always edited as you see fit according to the inputted prompt. If they did not input a proper ToS, let them know within this JSON strucutre"},
                        {"role": "user", "content":

f"""
Give the following summary of the this inputted Terms of Service in the JSON structure below. Do note that the lenght of the arrays within this JSON are variable and can be changed as you see fit depending on the length of the summarized ToS. Within the key value pair of the JSON structure, always switch out the placeholder value with your input and only return a reply within this JSON strucutre and nothing else at all, no matter what is the input, the 3 dots represents data to be added:
{
    {
    "summary_title":"title here...", 
    "summary_meaning":"extension of the summary to elaborate it, including exact quotations from the ToS that you got the summary from..."
    },
    "grade":"grade of ToS according to ToS;DR's grading system, letters from A to E..."
}
Terms of Service inputted part {chunk_index}: {text_input}
"""}
                ]).choices[0].message.content # Accessing the answer of the request in a non streaming manner as Vercel does not support this for python flask runtime
                
                all_results.append(result_chunk)

            return jsonify({"result": all_results}), 200


@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code


if __name__ == "__main__":
    app.debug = True
    app.run()