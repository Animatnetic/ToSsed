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

        all_summary_headings = []
        all_extended_summaries = []

        if text_input == "" or text_input is None:
            return jsonify({"result": None}), 200 # Returning nothing has to not waste tokens/computation on empty inputs.
        else:
            max_chunk_size = 1500 # Tokens, in this case of which is "characters"
            chunks = [text_input[i: i+max_chunk_size] for i in range(0, len(text_input), max_chunk_size)] # Breaks up the input into chunks of 1500 characters intervals to operate them individually


            for chunk_index, chunk in enumerate(chunks):
                # result_chunk = client.chat.completions.create(
                #     model=model_name, 
                #     messages=[
                #         {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair. You only return data in JSON format with the value within the key value pair always edited as you see fit according to the inputted prompt. If they did not input a proper ToS, let them know within this JSON strucutre"},
                #         {"role": "user", "content":
                #             f"""
                #             Give the following summary of the this inputted Terms of Service in the JSON structure below. Do note that the lenght of the arrays within this JSON are variable and can be changed as you see fit depending on the length of the summarized ToS. Within the key value pair of the JSON structure, always switch out the placeholder value with your input and only return a reply within this JSON strucutre and nothing else at all, no matter what is the input, the 3 dots represents data to be added:

                #             {{
                #                 "summary_title": "A brief summary of this part of the terms of service highlighting only the more unfair/concerning part of the ToS",
                #                 "summary_meaning": "A more in-depth elaboration of the summary and what it means, as well as the specific quotations sourced from the Terms of Service"
                #             }}
                #             """
                # }]).choices[0].message.content # Accessing the answer of the request in a non streaming manner as Vercel does not support this for python flask runtime
                

                # Instead of returning whole JSON data, which may be more difficult for the AI, I will simply only return individual components.

                # all_results.append(result_chunk)
                # all_results = "".join(all_results)

                summary_heading = client.chat.completions.create(
                    model=model_name, 
                    messages=[
                        {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair"}, 
                        {"role": "user", "content": f"Give a very simplified summary for this chunk read of the Terms of Service: {chunk}"}
                    ]
                ).choices[0].message.content

                extended_summary = client.chat.completions.create(
                    model=model_name, 
                       messages=[
                        {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair"}, 
                        {"role": "user", "content": f"Give an extended, more elaborate summary for this chunk read of the Terms of Service, include exact quotes for evidence from the ToS to backup your claim: {chunk}"}
                    ]
                ).choices[0].message.content

                all_summary_headings.append(summary_heading)
                all_extended_summaries.append(extended_summary)

                # print(all_results)
            
            # grade_result

            grade = client.chat.completions.create(
                model=model_name, 
                    messages=[
                    {"role": "system", "content": "You are a terms of service summarizer, pretty much, a legal expert to help normal people to understand key points of the ToS, especially those of which breach the user's rights and are most unfair"}, 
                    {"role": "user", "content": f"Only output one letter,from A to E to grade the fairness of this ToS based off of these summary points: {" ".join(all_summary_headings)}"}
                ]
            ).choices[0].message.content

            return jsonify({"summary_headings": all_summary_headings, "summary_extensions": all_extended_summaries, "grade": grade}), 200


@app.errorhandler(404)
def page_not_found(error_message):
    return jsonify({"status": 404, "message": "Not Found"}), 404 # Error 404 code


if __name__ == "__main__":
    app.debug = True
    app.run()


f"""
Analyze the following part of a medical report and extract key information.
Return the results in a JSON format with the following structure:
{{
    "summary": "A brief summary of this part of the report",
    "abnormal_results": [
        {{"test_name": "Test Name", "value": "Abnormal Value", "reference_range": "Normal Range", "interpretation": "Brief interpretation"}}
    ],
    "charts": [
        {{
            "chart_type": "bar",
            "title": "Chart Title",
            "data": [
                {{"label": "Category1", "value1": Number1, "value2": Number2, ...}},
                {{"label": "Category2", "value1": Number1, "value2": Number2, ...}},
                ...
            ]
        }},
        {{
            "chart_type": "area",
            "title": "Chart Title",
            "x_axis_key": "month",
            "data_keys": ["value1", "value2", ...],
            "data": [
                {{"month": "January", "value1": Number1, "value2": Number2, ...}},
                {{"month": "February", "value1": Number1, "value2": Number2, ...}},
                ...
            ],
            "trend_percentage": 5.2,
            "date_range": "January - June 2024"
        }}
    ],
    "recommendations": ["Recommendation 1", "Recommendation 2", ...]
}}

Medical Report Part {i+1}/{len(chunks)}:
{chunk}
"""