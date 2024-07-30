import os
import json
import asyncio
import aiohttp
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
async def summarize_input():
    if request.method == "GET":
        text_input = request.args.get("input")

        if text_input == "" or text_input is None:
            return jsonify({"result": None}), 200 # Returning nothing as to not waste tokens/computation on empty inputs.
        else:
            all_results = []
            all_summary_titles = [] # Is considered by the Falcon to give a grading bsed on the titles of the most major/important points of the summarised ToS.
            max_chunk_size = 500 # Tokens, in this case, is "characters"
            chunks = [text_input[i: i+max_chunk_size] for i in range(0, len(text_input), max_chunk_size)] # Breaks up the input into chunks of 1500 characters intervals to operate them individually

            headers = {
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {API_KEY}"
            }


            async with aiohttp.ClientSession() as session: 
                for chunk_index, chunk in enumerate(chunks):
                    summary_chunk_payload = {
                        "model": model_name, 
                        "messages": [
                        {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair. You only return data in JSON format with the value within the key value pair always edited as you see fit according to the inputted prompt. If they did not input a proper ToS, let them know within this JSON strucutre. Do not summarize everything, only the more concerning components of the ToS, and only those more concerning ones"},
                        {"role": "user", "content":
                            f"""
                            Give the following summary of the this inputted Terms of Service in the JSON structure below:

                            {{"summary_title": "A brief summary of this part of the terms of service highlighting only the more unfair/concerning part of the ToS", "summary_meaning": "A more in-depth elaboration of the summary and what it means, as well as the specific quotations sourced from the Terms of Service, ensure to incase in quotation marks to make those quotes explicit"}}

                            prompt: {chunk}
                        """}
                                    ]
                    }
                    async with session.post(API_URL, headers=headers, json=summary_chunk_payload) as response:
                        result = await response.json()

                    result_chunk = result["choices"][0]["message"]["content"]
                    result_chunk = result_chunk[1:len(result_chunk)]
                    result_chunk = json.loads(result_chunk)

                    all_summary_titles.append(result_chunk["summary_title"])
                    all_results.append(result_chunk)

                # A request for the grading of the inputted Terms of Service.
                tos_grading_payload = {
                    "model": model_name, 
                    "messages": [
                        {"role": "system", "content": "You are a terms of service grader, giving only a letter or 'Ungraded' as a response to inputted ToS summary titles."},
                        {"role": "user", "content":
                            f"""
                            ONLY OUTPUT ONE LETTER OR "Ungraded", nothing else
                            Give a letter from A to E, like the classification system of a website called ToS; DR, to grade the fairness of this inputted ToS. (Or write "Ungraded" if it is not a valid ToS).

                            ToS summary overview: {"".join(all_summary_titles)}
                        """}
                    ]
                }
            
                async with session.post(API_URL, headers=headers, json=tos_grading_payload) as grade_response:
                    grade_result_json = await grade_response.json()

                grade = grade_result_json["choices"][0]["message"]["content"]
                grade = grade[1:len(grade)] # Remove blank text at the very start
            
            return jsonify({"all_summaries": all_results, "grade": grade}), 200


@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code


if __name__ == "__main__":
    app.run()
