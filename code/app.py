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
    must_match = args.get("include", default="").lower()
    dont_match = args.get("exclude", default="").lower()

    known_positions_not = args.get("exclude_pos", default="{}").lower()
    known_positions_not = json.loads(known_positions_not)

    known_positions = args.get("include_pos", default="{}").lower()
    known_positions = json.loads(known_positions)

    wordlist_wordle_only = args.get("wordlist", default="wordle_all") == "wordle_all"

    algorithm = args.get("algorithm", default="frequency")

    query = {
        "known_positions_not": known_positions_not,
        "known_positions": known_positions,
        "must_match": must_match,
        "dont_match": dont_match,
        "algorithm": algorithm,
    }

    resp = {
        "words": solver.guess(solver.wordlist(wordlist_wordle_only), **query),
        "nonce": nonce,
    }

    if args.get("show_query", default="false") != "false":
        resp["query"] = query

    return resp
