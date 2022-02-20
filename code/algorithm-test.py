from hashlib import algorithms_available
from operator import add
import solver
import json
import datetime


def add_to_dict(dict, key, sub_key, value):
    if key not in dict:
        dict[key] = {}
    dict[key][sub_key] = value


def replace_char(string, index, char):
    return string[:index] + char + string[index + 1 :]


def chars_in_colour(colour, as_padded_str=False):
    by_col = {}
    for row in colour:
        for col in colour[row]:
            by_col[col] = colour[row][col]
    if as_padded_str:
        padded_str = ""
        for i in range(0, len(by_col)):
            if str(i) in by_col:
                padded_str += by_col[str(i)]
            else:
                padded_str += "_"
        return padded_str

    return by_col


def intersect_strings(a, b):
    result = ""
    for c in range(0, len(a)):
        if a[c] == b[c]:
            result += a[c]
        else:
            result += "_"
    return result


def get_cell_colour(word, guess, col):
    g = guess[col]
    w = word[col]
    if g == w:
        return "green"
    if g not in word:
        return 'grey'        
    if g in intersect_strings(word, guess):
        return 'grey'
    if guess.count(g) > word.count(g) and guess.find(g) < col:
        return 'grey'
        
    return 'orange'


def solve(wordlist, word, algorithm="frequency", annotate=False):
    grey = {}
    green = {}
    orange = {}

    for try_number in range(0, 101):
        guessed_dict = solver.guess(
            wordlist=wordlist,
            grey=grey,
            green=green,
            orange=orange,
            algorithm=algorithm,
        )
        if annotate:
            print(try_number)
            print("green", json.dumps(green))
            print("orange", json.dumps(orange))
            print("grey", json.dumps(grey))
            print(
                f"http://127.0.0.1:5000/solve?green={json.dumps(green)}&orange={json.dumps(orange)}&grey={json.dumps(grey)}&show_query=1"
            )

        if len(guessed_dict) == 0:
            print(f"No words found for {word}, using: {algorithm}")
            return -1
        guessed = next(iter(guessed_dict))
        # print("\t" + guessed)
        if annotate:
            print(f"\t{word}\tguess:{guessed}")
        if guessed == word:
            return try_number
        for char_pos, char in enumerate(guessed):
            cell_colour = get_cell_colour(word, guessed, char_pos)
            row = str(try_number)
            if cell_colour == "green":
                add_to_dict(green, row, str(char_pos), char)
            elif cell_colour == "orange":
                add_to_dict(orange, row, str(char_pos), char)
            elif cell_colour == "grey":
                add_to_dict(grey, row, str(char_pos), char)

    return -1


def run_test(algorithm="frequency", wordlist_all=False):
    wordlist = solver.wordlist(wordlist_all=wordlist_all)
    wordle_valid = solver.wordlist(wordlist_all=False)

    tries_total = 0
    wins = 0
    loses = 0

    for i, word in enumerate(wordle_valid):
        tries = solve(wordlist, word, algorithm)
        # print(f"{i}: {word}. Tries: {tries}. Algorithm: {algorithm}")
        if tries >= 0:
            tries_total += tries
            wins += 1
        else:
            print(
                f"{word} not solved. guesses: {tries} Algorithm: {algorithm} Full_Wordlist: {wordlist_all}"
            )
            loses += 1

    print(
        f"Average tries: {tries_total / wins}, loses: {loses}, algorithm: {algorithm}, wordlist_all: {wordlist_all}"
    )
    return {
        "wins": wins,
        "loses": loses,
        "tries": tries_total,
        "average_tries": tries_total / wins,
        "algorithm": algorithm,
        "wordlist_all": wordlist_all,
    }


def run_all_tests(algorithms):
    all_results = []
    for algorithm in algorithms:
        for wordlist_all in [True, False]:
            results = run_test(algorithm, wordlist_all)
            all_results.append(results)
            print(results)

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    with open(f"../results-{suffix}.json", "w") as outfile:
        json.dump(all_results, outfile, indent=4)

    return all_results


if __name__ == "__main__":
    algorithms_available = [
        "frequency",
        "position_and_frequency",
        "position_and_frequency_unique",
        "combo",
        "random",
        "combo_num_words",
        "entropy",
    ]

    # run_all_tests(algorithms_available)

    run_test(algorithms_available[6], wordlist_all=False)

    # wordlist = solver.wordlist(False)
    # print(solve(wordlist, "igloo", "entropy", True))
    # print(solve(wordlist, "utter", "entropy", True))
    # # run_test("frequency",False)
