from audioop import add
import math
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
    dont_match = "".join(dont_match)
    for word in words:
        letter_not_found = True
        for letter in dont_match:
            letter_not_found = letter_not_found and letter not in word

        if letter_not_found:
            filtered.append(word)

    return filtered


@cached
def filter_dont_match_at_pos(words, grey):
    filtered = []
    for word in words:
        add_word = True
        for row in grey:
            for col in grey[row]:
                if word[int(col)] == grey[row][col]:
                    add_word = False
                    break
            if not add_word:
                break
        if add_word:
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
def filter_green(words, green):
    filtered2 = []
    for word in words:
        matches = True
        for key, value in green.items():
            matches = matches and word[int(key)] == value
            if not matches:
                break

        if matches:
            filtered2.append(word)

    return set(filtered2)


@cached
def filter_orange(words, orange):
    filtered2 = []
    for word in words:
        word_good = True
        for key, value in orange.items():
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
def sort_wordlist_position_frequency(words, favour_unique=True):
    freq = char_frequency_by_position(words)
    ranked = {}
    for word in words:
        ranked[word] = 0
        num_letters = favour_unique and 1 or len(word)
        for i, char in enumerate(word):
            ranked[word] += freq[i][char] * num_letters
    return dict(sorted(ranked.items(), key=lambda item: -item[1]))


@cached
def sort_wordlist_entropy(words):
    freq = char_frequency(words)
    chars_total = sum(freq.values())
    ranked = {}
    for word in words:
        ranked[word] = 0
        for char in set(word):
            ranked[word] += -(
                freq[char] / chars_total * math.log(freq[char] / chars_total, 2)
            )
    return dict(sorted(ranked.items(), key=lambda item: -item[1]))


@cached
def sort_wordlist(words, algorithm="frequency"):
    if algorithm == "position_and_frequency":
        return sort_wordlist_position_frequency(words, favour_unique=False)
    elif algorithm == "entropy":
        return sort_wordlist_entropy(words)
    elif algorithm == "position_and_frequency_unique":
        return sort_wordlist_position_frequency(words)
    elif algorithm == "combo":
        bypos = sort_wordlist_position_frequency(words)
        byfreq = sort_wordlist_frequency(words)
        merged = {}
        for word in bypos:
            merged[word] = bypos[word] * bypos[word] * byfreq[word]
        return dict(sorted(merged.items(), key=lambda item: -item[1]))
    elif algorithm == "combo_num_words":
        bypos = sort_wordlist_position_frequency(words)
        byfreq = sort_wordlist_frequency(words)
        merged = {}
        for word in bypos:
            merged[word] = bypos[word] + byfreq[word] / (
                1 + math.log(1 + len(words))
            )  # looks good :)
        return dict(sorted(merged.items(), key=lambda item: -item[1]))

    elif algorithm == "frequency":
        return sort_wordlist_frequency(words)
    elif algorithm == "random":
        ranked = {}
        for word in words:
            ranked[word] = randint(0, len(words))
        return dict(sorted(ranked.items(), key=lambda item: -item[1]))

    return {}


@cached
def match_all_chars(filtered, chars_mandatory):
    filtered2 = []
    for word in filtered:
        word_copy = word
        word_good = True
        for char in chars_mandatory:
            if char in word_copy:
                word_copy = word_copy.replace(char, "_", 1)
                word_good = word_good and True
            else:
                word_good = False
                break
        if word_good:
            filtered2.append(word)
    return filtered2


def chars_to_exclude(grey, green, orange):
    dont_match = []
    for ele in grey.values():
        dont_match.extend(ele.values())
    for x in green.values():
        for c in x.values():
            if c in dont_match:
                dont_match.remove(c)
    for x in orange.values():
        for c in x.values():
            if c in dont_match:
                dont_match.remove(c)
    return dont_match


@cached
def guess(
    wordlist,
    grey={},
    green={},
    orange={},
    algorithm="frequency",
):

    filtered = wordlist
    if grey:
        dont_match = chars_to_exclude(grey, green, orange)
        filtered = filter_dont_match(filtered, dont_match)

    known_positions = []

    for row in range(0, 5):
        row = str(row)
        chars_mandatory = []
        if row in green:
            filtered = filter_green(filtered, green[row])
            chars_mandatory.extend(green[row].values())
            known_positions.extend(green[row].keys())
        if row in orange:
            filtered = filter_orange(filtered, orange[row])
            chars_mandatory.extend(orange[row].values())

        filtered = match_all_chars(filtered, chars_mandatory)

        filtered = filter_dont_match_at_pos(filtered, grey)

    filtered = sort_wordlist(filtered, algorithm=algorithm)

    return filtered
