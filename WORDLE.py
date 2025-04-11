from wordfreq import word_frequency
import nltk
import os
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

def satisfy_con(word, condition, previous):
    if not (previous and condition):
        return True
    musts = set(previous[idx].lower() for idx, hint in enumerate(condition) if hint in ['g', 'y'])
    for idx, hint in enumerate(condition):
        if (
                (hint == 'g' and word[idx].lower() != previous[idx].lower())
                or
                (hint == 'y' and (
                        (previous[idx].lower() not in word.lower()) or (word[idx].lower() == previous[idx].lower())))
                or
                (hint == 'd' and previous[idx].lower() in word.lower() and (
                        (previous[idx].lower() not in musts) or previous[idx] == word[idx]))
        ):
            return False
    return True

def get_n_letter_words(length, language='en', min_freq=0) -> list[str]:
    from nltk.corpus import words
    nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
    if not os.path.exists(os.path.join(nltk_data_path, 'corpora', 'words')):
        nltk.download('words', quiet=True)
    word_list = words.words()
    n_letter_words = []
    for word in word_list:
        if len(word) == length and word.isalpha():
            freq = word_frequency(word, language)
            if freq >= min_freq:
                n_letter_words.append((word, freq))
    n_letter_words.sort(key=lambda x: x[1], reverse=True)
    words = list(wd[0] for wd in n_letter_words)
    return words


if __name__ == "__main__":
    n = int(input("Specify the length of the word: "))
    guess_round = 1
    con = ''
    possibles = get_n_letter_words(length=n)
    # print('corer' in possibles)
    while True:
        if len(possibles) == 0:
            print("I quit! Can't figure it out!\n")
            n = int(input("Specify the length of the word: "))
            guess_round = 1
            con = ''
            possibles = get_n_letter_words(length=n)
            continue
        print('-' * 40 + f'Round {guess_round}' + '-' * 40)
        guess = possibles[0]
        print(f"My guess is: {guess}")
        con = input("Hint me (`d`: Dark, `y`: Yellow, `g`: Green): ").lower()
        if all(i not in ['g', 'd', 'y'] for i in con) or con == 'g'*n:
            print("You bet!\n")
            n = int(input("Specify the length of the word: "))
            guess_round = 1
            con = ''
            possibles = get_n_letter_words(length=n)
            continue
        guess_round += 1
        possibles = [possible for possible in possibles if satisfy_con(possible, con, guess)]