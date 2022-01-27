import os



with open(os.path.dirname(os.path.abspath(__file__)) + '/wordlist.txt', 'r') as file:
    data = file.read()

wordlist = data.split("\n")


def char_frequency(wordlist):
    txt = "".join(wordlist)
    freq = {}
    for char in txt:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    
    return dict(sorted(freq.items(), key=lambda item: -item[1]))


def filter_dont_match(wordlist, dont_match):    
    filtered = []
    for word in wordlist:
        letter_not_found = True
        for letter in dont_match:
            letter_not_found = letter_not_found and letter not in word

        if letter_not_found:
            filtered.append(word)

    return filtered


def filter_known_letters(wordlist, must_match):
    filtered2 = []
    for word in wordlist:
        all_match = True
        for char in must_match:
            all_match = all_match and char in word
        if all_match:
            filtered2.append(word)
    return set(filtered2)

def filter_known_positions(wordlist, known_positions):
    filtered2=[]
    for word in wordlist:
        matches = True
        for key, value in known_positions.items():
            matches = matches and word[int(key)] == value
            
        if matches:
            filtered2.append(word)
            
    return set(filtered2)


def filter_known_positions_not(wordlist, known_positions_not):
    filtered2 = []
    for word in wordlist:
        word_good = True
        for item in known_positions_not:
            key = next(iter(item))
            value = item[key]
            word_good = word_good and word[int(key)] != value
        
        if word_good:
            filtered2.append(word)
            
    return set(filtered2)


def sort_by_frequency(words):
    freq = char_frequency(words)
    ranked = {}
    for word in words:
        ranked[word] = 0
        chars = set(word)
        for char in chars:
            ranked[word] += freq[char] * len(chars)
    
    return dict(sorted(ranked.items(), key=lambda item: -item[1]))    




if __name__ == '__main__':
    must_match = 'ack'
    dont_match = 'lertmsony'

    known_positions = {
    0:'w',
#     1: 'n',
#     2:'a',
#     3:'c',
#     4:'k'
    }

    known_positions_not = [
    {0: 'a'},
#     {1: 'b'},
#     {0: 'k'},
#     {0: 'n'}
#     {2 :'n'},
#     {3: 'n'},
#     {4: 'a'}, 
    ]


    filtered = filter_dont_match(wordlist, dont_match)
    filtered = filter_known_letters(filtered, must_match)
    filtered = filter_known_positions(filtered, known_positions)
    filtered = filter_known_positions_not(filtered, known_positions_not)
    print(filtered)
