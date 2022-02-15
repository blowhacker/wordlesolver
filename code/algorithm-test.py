from hashlib import algorithms_available
import solver
import json
import datetime


def solve(wordlist, word, algorithm="frequency", annotate=False):
    dont_match = ""
    known_positions = {}
    known_positions_not = []

    for i in range(1, 7):
        guessed_dict = solver.guess(
            wordlist=wordlist,
            grey=dont_match,
            green=known_positions,
            orange=known_positions_not,
            algorithm=algorithm,
        )

        if len(guessed_dict) == 0:
            print("No words found")
            return -1
        guessed = next(iter(guessed_dict))
        if annotate:
            print(f"\t{guessed}")
        if guessed == word:
            return i
        for ii, char in enumerate(guessed):
            if char == word[ii]:
                known_positions[str(ii)] = char
            elif char in word:
                knp = {}
                knp[str(ii)] = char
                known_positions_not.append(knp)
            if char not in word:
                dont_match += char

    return -1


def run_test(algorithm="frequency", wordlist_all=False):
    wordlist = solver.wordlist(wordlist_all=wordlist_all)
    wordle_valid = solver.wordlist(wordlist_all=False)

    tries_total = 0
    wins = 0
    loses = 0

    for i, word in enumerate(wordle_valid):
        tries = solve(wordlist, word, algorithm)
        print(f"{i}: {word}. Tries: {tries}")
        if tries > 0:
            tries_total += tries
            wins += 1
        else:
            print(f"{word} not solved")
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

    all_results = []
    for algorithm in algorithms_available:
        for wordlist_all in [True, False]:
            results = run_test(algorithm, wordlist_all)
            all_results.append(results)
            print(results)

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    with open(f"../results-{suffix}.json", "w") as outfile:
        json.dump(all_results, outfile, indent=4)

    # run_test(algorithms_available[1], wordlist_all=False)

    # wordlist = solver.wordlist(False)
    # print(solve(wordlist, "tight", "position_and_frequency", True))
    # print(solve(wordlist, "ember", "random"))
