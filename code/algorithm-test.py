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


def get_chars_in_colour(colour):
    by_col = {}
    for row in colour:
        for col in colour[row]:
            by_col[col] = colour[row][col]

    return by_col


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
        # print(try_number)
        # print("green", json.dumps(green))
        # print("orange", json.dumps(orange))
        # print("grey", json.dumps(grey))
        print(
            f"http://127.0.0.1:5000/solve?green={json.dumps(green)}&orange={json.dumps(orange)}&grey={json.dumps(grey)}&show_query=1"
        )

        if len(guessed_dict) == 0:
            print(f"No words found for {word}, using: {algorithm}")
            return -1
        guessed = next(iter(guessed_dict))
        print(guessed)
        if annotate:
            print(f"\t{word}\tguess:{guessed}")
        if guessed == word:
            return try_number
        for char_pos, char in enumerate(guessed):
            row = str(try_number)
            if char == word[char_pos]:
                add_to_dict(green, row, str(char_pos), char)
            if char not in word or (
                char in get_chars_in_colour(green).values() and char != word[char_pos]
            ):
                add_to_dict(grey, row, str(char_pos), char)
            elif char in replace_char(word, char_pos, "_") and char != word[char_pos]:
                add_to_dict(orange, row, str(char_pos), char)

    return -1


def run_test(algorithm="frequency", wordlist_all=False):
    wordlist = solver.wordlist(wordlist_all=wordlist_all)
    wordle_valid = solver.wordlist(wordlist_all=False)

    tries_total = 0
    wins = 0
    loses = 0

    for i, word in enumerate(wordle_valid):
        tries = solve(wordlist, word, algorithm)
        print(f"{i}: {word}. Tries: {tries}. Algorithm: {algorithm}")
        if tries > 0:
            tries_total += tries
            wins += 1
        else:
            print(f"{word} not solved. guesses: {tries} Algorithm: {algorithm}")
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

    # run_test(algorithms_available[1], wordlist_all=False)

    wordlist = solver.wordlist(True)
    print(solve(wordlist, "enter", "entropy", False))
    # run_test("frequency",False)
