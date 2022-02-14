import solver


def solve(wordlist, word, sort_by_pos=True):
    dont_match = ""
    must_match = ""
    known_positions = {}
    known_positions_not = []

    for i in range(1, 7):
        must_match = "".join(set(must_match))
        guessed_dict = solver.guess(
            wordlist=wordlist,
            dont_match=dont_match,
            must_match=must_match,
            known_positions=known_positions,
            known_positions_not=known_positions_not,
            sort_by_pos=sort_by_pos,
        )

        if len(guessed_dict) == 0:
            print("No words found")
            return -1
        guessed = next(iter(guessed_dict))
        if guessed == word:
            return i
        for ii, char in enumerate(guessed):
            if char == word[ii]:
                known_positions[str(ii)] = char
                must_match += char
            elif char in word:
                knp = {}
                knp[str(ii)] = char
                known_positions_not.append(knp)
                must_match += char
            if char not in word:
                dont_match += char

    return -1


def run_test(sort_by_pos=True, wordlist_all=False):
    wordlist = solver.wordlist(wordlist_all=wordlist_all)
    wordle_valid = solver.wordlist(wordlist_all=False)

    tries_total = 0
    wins = 0
    loses = 0

    for i, word in enumerate(wordle_valid):
        tries = solve(wordlist, word, sort_by_pos=sort_by_pos)
        print(f"{i}: {word}. Tries: {tries}")
        if tries > 0:
            tries_total += tries
            wins += 1
        else:
            print(f"{word} not solved")
            loses += 1

    print(
        f"Average tries: {tries_total / wins}, loses: {loses}, sort_by_pos: {sort_by_pos}, wordlist_all: {wordlist_all}"
    )


if __name__ == "__main__":
    # run_test(True, wordlist_all=False)

    wordlist = solver.wordlist(True)
    print(solve(wordlist, "gaunt", True))
