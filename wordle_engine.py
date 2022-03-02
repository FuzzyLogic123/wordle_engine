#Iterate over every possible first guess (using wordles predefined answsers as a sample space).
#For each of these check the pattern it gives and hence the amount by which the number of possible words is reduced by (calculate the bits each guess provides)
from math import log2
from game_functions import get_pattern, valid_entries

with open('./data/wordle_answers.txt') as file:
    legal_words = [ line.strip() for line in file ]

legal_words_copy = legal_words.copy()

def remove_at(i, s):
    return s[:i] + s[i+1:]

def check_remaining_words(previous_guess, pattern, legal_words):
    valid_word_count = 0
    valid_word_list = []
    for word in legal_words:
        if is_valid(word, pattern, previous_guess):
            valid_word_count += 1
            valid_word_list += [word]
    return (valid_word_count, valid_word_list)

def is_valid(word, pattern, previous_guess):
    """checks if word is valid given evaluation"""
    #checks green by finding indexes where green letter is found
    word = list(word)
    word_copy = word.copy()
    green_indexes = [pos for pos, char in enumerate(pattern) if char == '2']
    for index in green_indexes:
        if word[index] != previous_guess[index]:
            return False
        else:
            word_copy.remove(previous_guess[index])
    
    #finds yellow letters indexes
    yellow_indexes = [pos for pos, char in enumerate(pattern) if char == '1']
    for index in yellow_indexes:
        if previous_guess[index] not in word_copy or previous_guess[index] == word[index]:
            return False
        else:
            word_copy.remove(previous_guess[index])

    grey_indexes = [pos for pos, char in enumerate(pattern) if char == '0']
    for index in grey_indexes:
        if previous_guess[index] in word_copy:
            return False
    return True

def get_information_count(word_under_evaluation, answer, legal_words):
    pattern = get_pattern(word_under_evaluation, answer)
    remaining_word_count = check_remaining_words(word_under_evaluation, pattern, legal_words)[0]

    return log2( len(legal_words) / remaining_word_count )

def get_new_list(guess, pattern, legal_words):
    return check_remaining_words(guess, pattern, legal_words)[1]

def get_best_guess(pattern, previous_guess, legal_words, slow = False):
    first_guess = 'crate'
    if not previous_guess: return ([first_guess, 'a lot of'], legal_words)
    legal_words = get_new_list(previous_guess, pattern, legal_words)
    #cheat and return precalculated answers for common patterns that have been pre-calculated
    if previous_guess == first_guess:
        if pattern == '00000':
            return (['solid', '5.458734731026386'], legal_words)
        elif pattern == '00002':
            return (['sling', '5.181665650683946'], legal_words)
    # if len(legal_words) <= 10:
        # words_to_evaluate = valid_entries
    if slow or len(legal_words) <= 30:
        words_to_evaluate = legal_words_copy
    else:
        words_to_evaluate = legal_words
    word_score = []
    for word_under_evaluation in words_to_evaluate:
        #checks across every hypothetical solution
        total_information = 0
        for answer in legal_words:
            information_per_word = get_information_count(word_under_evaluation, answer, legal_words)
            # print(information_per_word)
            total_information += information_per_word
        word_score.append([word_under_evaluation, total_information / len(legal_words)])
    # print(word_score)
    word_score_sorted = sorted(word_score, key=lambda word_eval: word_eval[1], reverse = True)
    highest_bits_answer = word_score_sorted[0]
    for word in word_score_sorted:
        if word[0] in legal_words:
            best_viable_answer = word
            break
    if best_viable_answer[1] == highest_bits_answer[1]:
        return (best_viable_answer, legal_words)
    return (highest_bits_answer, legal_words)

    # if len(legal_words) <= 2:
    #     return ([legal_words[0], str(len(legal_words) - 1)], legal_words)
    # return (highest_bits_answer, legal_words)