import functions_framework
import openai

from flask import Flask, request, jsonify
from flask_cors import cross_origin


app = Flask(__name__)
openai.api_key = "ADD YOUR API KEY HERE"

@functions_framework.http
@cross_origin()
@app.route('/advdecomp', methods=['GET'])
def advdecomp(request):
    request_args = request.args

    if request_args and 'claim' in request_args:
        claim = request_args['claim']
    else:
        claim = 'No Claim'

    if request_args and 'justification' in request_args:
        justification = request_args['justification']
    else:
        justification = "No Justification"

    return predictFineTuned(claim, justification)


def predictFineTuned(claim, justification):
    response = openai.Completion.create(
            model="davinci:ft-personal:train-append-subq-2023-03-27-18-47-21",
            prompt= claim + "\nsub-question:",
            temperature=0.2,
            max_tokens=128,
            top_p=0.75,
            frequency_penalty=1,
            presence_penalty=1,
            stop=["END"],
            best_of=2,
        )
    prediction = response.choices[0].text
    return jsonify(prediction)