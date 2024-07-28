import os
import json
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
def summarize_input():
    if request.method == "GET":
        text_input = request.args.get("input")
        
        all_results = []

        if text_input == "" or text_input is None:
            return jsonify({"result": None}), 200 # Returning nothing has to not waste tokens/computation on empty inputs.
        else:
            max_chunk_size = 1500 # Tokens, in this case, is "characters"
            chunks = [text_input[i: i+max_chunk_size] for i in range(0, len(text_input), max_chunk_size)] # Breaks up the input into chunks of 1500 characters intervals to operate them individually

            for chunk_index, chunk in enumerate(chunks):
                result_chunk = client.chat.completions.create(
                    model=model_name, 
                    messages=[
                        {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair. You only return data in JSON format with the value within the key value pair always edited as you see fit according to the inputted prompt. If they did not input a proper ToS, let them know within this JSON strucutre. Do not summarize everything, only the more concerning components of the ToS, and only those more concerning ones"},
                        {"role": "user", "content":
                            f"""
                            Give the following summary of the this inputted Terms of Service chunk in the JSON structure below:

                            {{"summary_title": "A brief summary of this part of the terms of service highlighting only the more unfair/concerning part of the ToS", "summary_meaning": "A more in-depth elaboration of the summary and what it means, as well as the specific quotations sourced from the Terms of Service, ensure to incase in quotation marks to make those quotes explicit"}}

                            prompt: {chunk}
                            """
                }]).choices[0].message.content # Accessing the answer of the request in a non streaming manner as Vercel does not support this for python flask runtime

                # result_chunk = result_chunk[1:len(result_chunk)] # Removing that first empty character that is always strangely present on the completions message given by falcon
                # result_chunk = json.loads(result_chunk) # Converting returned stirng into json, but can not return this directly as flask needs to return a specific Response object

                # return jsonify({"summary_title": result_chunk["summary_title"], "summary_meaning": result_chunk["summary_meaning"]}), 200 # Unpacking dictionary into a json structure that is actually returned 
                all_results.append(result_chunk)

            all_results = "".join(all_results)
            all_results = all_results[1:len(all_results)]
            all_results = json.loads(all_results)
            
            return jsonify({"summary_title": all_results["summary_title"], "summary_meaning": all_results["summary_meaning"]}), 200
            # This is returning all in one go. Though, this may even exceed 1 minute response...



@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code


if __name__ == "__main__":
    app.debug = True
    app.run()
