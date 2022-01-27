from email.policy import default
import json
from flask import Flask, request, render_template
import solver

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/solve")
def solve():
    args = request.args
    must_match = args.get('include', default="")
    dont_match = args.get('exclude', default="")

    known_positions_not = args.get('exclude_pos', default="{}")
    known_positions_not = json.loads(known_positions_not)

    known_positions = args.get('include_pos', default="{}")
    known_positions = json.loads(known_positions)


    filtered = solver.filter_dont_match(solver.wordlist, dont_match)
    filtered = solver.filter_known_letters(filtered, must_match)
    
    filtered = solver.filter_known_positions(filtered, known_positions)
    
    filtered = solver.filter_known_positions_not(filtered, known_positions_not)
    

    filtered = solver.sort_by_frequency(filtered)

    return {'words': list(filtered)}
    # return known_positions
