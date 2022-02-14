import os
from random import randint
from memoization import cached


@cached
def wordlist(wordlist_all=False):
    file = "wordle-allowed.txt" if wordlist_all else "wordle-solutions.txt"
    with open(os.path.dirname(os.path.abspath(__file__)) + "/" + file, "r") as file:
        data = file.read()

    return data.split("\n")


@cached
def char_frequency(words):
    freq = {}
    for word in words:
        for char in word:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1

    return dict(sorted(freq.items(), key=lambda item: -item[1]))


@cached
def char_frequency_by_position(words):
    freq = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
    for word in words:
        for i, char in enumerate(word):
            if char in freq[i]:
                freq[i][char] += 1
            else:
                freq[i][char] = 1
    for i in range(0, 5):
        freq[i] = dict(sorted(freq[i].items(), key=lambda item: -item[1]))
    return freq


@cached
def filter_dont_match(words, dont_match):
    filtered = []
    for word in words:
        letter_not_found = True
        for letter in dont_match:
            letter_not_found = letter_not_found and letter not in word

        if letter_not_found:
            filtered.append(word)

    return filtered


@cached
def filter_known_letters(words, must_match):
    filtered2 = []
    for word in words:
        all_match = True
        for char in must_match:
            all_match = all_match and char in word
        if all_match:
            filtered2.append(word)
    return set(filtered2)


@cached
def filter_known_positions(words, known_positions):
    filtered2 = []
    for word in words:
        matches = True
        for key, value in known_positions.items():
            matches = matches and word[int(key)] == value
            if not matches:
                break

        if matches:
            filtered2.append(word)

    return set(filtered2)


@cached
def filter_known_positions_not(words, known_positions_not):
    filtered2 = []
    for word in words:
        word_good = True
        for item in known_positions_not:
            key = next(iter(item))
            value = item[key]
            word_good = word_good and word[int(key)] != value

        if word_good:
            filtered2.append(word)

    return set(filtered2)


@cached
def sort_wordlist_frequency(words):
    freq = char_frequency(words)
    ranked = {}
    for word in words:
        ranked[word] = 0
        num_letters = len(set(word))
        for char in word:
            ranked[word] += freq[char] * num_letters
    return dict(sorted(ranked.items(), key=lambda item: -item[1]))


@cached
def sort_wordlist_position_frequency(words):
    freq = char_frequency_by_position(words)
    ranked = {}
    for word in words:
        ranked[word] = 0
        num_letters = len(set(word))
        for i, char in enumerate(word):
            ranked[word] += freq[i][char] * num_letters
    return dict(sorted(ranked.items(), key=lambda item: -item[1]))


@cached
def sort_wordlist(words, algorithm="frequency"):
    if algorithm == "position_and_frequency":
        return sort_wordlist_position_frequency(words)
    elif algorithm == "frequency":
        return sort_wordlist_frequency(words)
    elif algorithm == "random":
        ranked = {}
        for word in words:
            ranked[word] = randint(0, len(words))

    return dict(sorted(ranked.items(), key=lambda item: -item[1]))


def guess(
    wordlist,
    dont_match="",
    must_match="",
    known_positions={},
    known_positions_not={},
    algorithm="frequency",
):

    filtered = filter_dont_match(wordlist, dont_match)
    filtered = filter_known_letters(filtered, must_match)
    filtered = filter_known_positions(filtered, known_positions)
    filtered = filter_known_positions_not(filtered, known_positions_not)
    filtered = sort_wordlist(filtered, algorithm=algorithm)

    return filtered
