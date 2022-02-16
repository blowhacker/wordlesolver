from hashlib import algorithms_available
import solver
import json
import datetime


def solve(wordlist, word, algorithm="frequency", annotate=False):
    grey = ""
    green = {}
    orange = {}

    for i in range(1, 7):
        guessed_dict = solver.guess(
            wordlist=wordlist,
            grey=grey,
            green=green,
            orange=orange,
            algorithm=algorithm,
        )

        if annotate:

            def rowprint(lst):
                str = ""
                for row in range(0, 5):
                    for col in range(0, 5):
                        if col in lst and row in lst[col]:
                            str += lst[row][col]
                        else:
                            str += "X"
                    str += "\n"
                print(str)

            rowprint(green)
            rowprint(orange)
            print("grey ", grey)
            # print("green ", green)
            # print("orange ", orange)

        if len(guessed_dict) == 0:
            print("No words found")
            return -1
        guessed = next(iter(guessed_dict))
        if annotate:
            print(f"\t{guessed}")
        if guessed == word:
            return i
        for char_pos, char in enumerate(guessed):
            k = str(i)
            if char == word[char_pos]:
                if k not in green:
                    green[k] = {}
                green[k][str(char_pos)] = char
            elif char in word:
                if str(i) not in orange:
                    orange[k] = {}
                orange[k][str(char_pos)] = char
            if char not in word:
                grey += char

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
    # algorithms_available = [
    #     "frequency",
    #     "position_and_frequency",
    #     "position_and_frequency_unique",
    #     "combo",
    #     "random",
    #     "combo_num_words",
    #     "entropy",
    # ]

    # all_results = []
    # for algorithm in algorithms_available:
    #     for wordlist_all in [True, False]:
    #         results = run_test(algorithm, wordlist_all)
    #         all_results.append(results)
    #         print(results)

    # suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    # with open(f"../results-{suffix}.json", "w") as outfile:
    #     json.dump(all_results, outfile, indent=4)

    # above this line is to iterate

    # run_test(algorithms_available[1], wordlist_all=False)

    wordlist = solver.wordlist(False)
    print(solve(wordlist, "refer", "random", True))
