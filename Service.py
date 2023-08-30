import json

from CohereSearch import search
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/answer", methods=['GET'])
def get_answer():
    args = request.args
    query = args["q"]

    if query is None or len(query) == 0:
        return app.response_class(
            response=json.dumps({"status": "No query present"}),
            status=200,
            mimetype="application/json"
        )

    answer, ref, context = search(query)
    return app.response_class(
            response=json.dumps({
                "answer": answer,
                "references": list(ref),
                "context": context
            }),
            status=200,
            mimetype="application/json"
        )
