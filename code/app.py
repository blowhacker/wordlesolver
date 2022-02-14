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

    filtered = solver.filter_dont_match(
        solver.wordlist(wordlist_wordle_only), dont_match
    )
    filtered = solver.filter_known_letters(filtered, must_match)

    filtered = solver.filter_known_positions(filtered, known_positions)

    filtered = solver.filter_known_positions_not(filtered, known_positions_not)

    sort_by_pos = args.get("sort_by_pos", default="byfreq") == "bypos"

    filtered = solver.sort_by_frequency(filtered, sort_by_pos)

    return {"words": filtered, "nonce": nonce}
