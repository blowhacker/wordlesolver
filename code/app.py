from cgitb import grey
from datetime import datetime
from email.policy import default
import json
from flask import Flask, request, render_template
import solver

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/olde")
def hello():
    return render_template("index.html")


@app.route("/")
def grid():
    return render_template("grid.html")


@app.route("/solve")
def solve():
    args = request.args
    nonce = args.get("nonce", default=datetime.now().timestamp())

    grey = args.get("grey", default="{}").lower()
    orange = args.get("orange", default="{}").lower()
    green = args.get("green", default="{}").lower()

    query = {
        "known_positions_not": json.loads(orange),
        "known_positions": json.loads(green),
        # "must_match": must_match,
        "dont_match": json.loads(grey),
        "algorithm": args.get("algorithm", default="frequency"),
    }

    wordlist_wordle_only = args.get("wordlist", default="wordle_all") == "wordle_all"
    resp = {
        "words": solver.guess(solver.wordlist(wordlist_wordle_only), **query),
        "nonce": nonce,
    }

    if args.get("show_query", default="false") != "false":
        resp["query"] = query

    return resp
