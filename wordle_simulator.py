import time
from game_functions import get_pattern
from wordle_engine import get_best_guess, legal_words

copy_of_legal_words = legal_words.copy()
number_of_guesses = 0
previous_guess = ''
pattern = ''
total_number_of_guesses = 0
failed_words = []
total_time = 0

for answer in legal_words:
    while True:
        number_of_guesses += 1
        t0 = time.time()
        best_guess_returned = get_best_guess(pattern, previous_guess, legal_words)
        t1 = time.time()
        total_time += t1-t0
        legal_words = best_guess_returned[1]
        previous_guess = best_guess_returned[0][0]
        pattern = get_pattern(previous_guess, answer)

        if all([letter_result == '2' for letter_result in pattern]):
            total_number_of_guesses += number_of_guesses
            print(f'{number_of_guesses} {answer}')
            break

        if number_of_guesses > 4:
            failed_words.append(answer)
            print(f'Failed {answer}')
            # break
    legal_words = copy_of_legal_words
    number_of_guesses = 0
    previous_guess = ''
    pattern = ''

print(f'{len(failed_words)} failures at {round(len(failed_words)/len(copy_of_legal_words)*100, 2)}%')
print(f'The average amount of guesses taken was {total_number_of_guesses / len(legal_words)}')
print(f'The average time taken per solution was {round(total_time / len(copy_of_legal_words), 2)}')
print('Words failed:')
print(failed_words)
print('slow mode was disabled...')