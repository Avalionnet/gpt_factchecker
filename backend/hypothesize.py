import functions_framework
import openai

from flask import Flask, request, jsonify
from flask_cors import cross_origin


app = Flask(__name__)
openai.api_key = "ADD YOUR API KEY HERE"

@functions_framework.http
@cross_origin()
@app.route('/hypothesize', methods=['GET'])
def hypothesize(request):
    request_args = request.args

    if request_args and 'question' in request_args:
        question = request_args['question']
    else:
        question = 'No question'

    return convert(question)

def convert(question):
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_hypothesis(question),
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )
    prediction = response.choices[0].text
    return jsonify(prediction)

def generate_hypothesis(question):
    return """You are a bot that converts binary sub-questions into a simple hypothesis.

sub-question:Did Russian military paratroopers land in Ukraine?
hypothesis:Russian military paratroopers landed in Ukraine

sub-question: Was the Russian landing near Kharkov?
hypothesis:The Russian landing was near Kharkov

sub-question:Did Donald Trump win the 2016 US-election?
hypothesis:Donald Trump won the 2016 US-election

sub-question:{}
hypothesis:
""".format(
        question
    )