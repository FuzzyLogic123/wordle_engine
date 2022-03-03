import time
from game_functions import delete_lines, get_pattern, get_input, print_coloured, print_word
from wordle_engine import get_best_guess, legal_words
from random import choice

# failed = ['crawl', 'crazy', 'fixer', 'foyer', 'gazer', 'graze', 'growl', 'gully', 'haunt', 'hilly', 'holly', 'hound', 'irate', 'joker', 'jolly', 'latch', 'maker', 'mammy', 'miner', 'moist', 'munch', 'offer', 'older', 'patch', 'payer', 'pound', 'rower', 'safer', 'savor', 'shape', 'shave', 'super', 'swear', 'tatty', 'taunt', 'truth', 'udder', 'vaunt', 'waste', 'watch', 'wight', 'willy', 'witch', 'witty', 'wooer', 'wound']
answer = choice(legal_words)
# answer = choice(failed)
# answer = 'hover'


user_guesses_count = 0
previous_guess = ''
pattern = ''
engine_enabled = False
manual_entry = False
slow = False

is_engine_enabled = input('Would you like to play with the engine enabled?\n')
is_engine_enabled = is_engine_enabled.split(' ')

engine_enabled = True if 'yes' in is_engine_enabled else False

manual_entry = True if 'manual' in is_engine_enabled else False

slow = True if 'slow' in is_engine_enabled else False


delete_lines()

while True:
    if engine_enabled:
        t0 = time.time()
        best_guess_returned = get_best_guess(pattern, previous_guess, legal_words, True) if slow else get_best_guess(pattern, previous_guess, legal_words)
        t1 = time.time()
        time_total = round(t1 - t0, 2)
        colour = 'red' if time_total > 5 else 'green'
        print_coloured(time_total, colour)
        print()
        best_guess = best_guess_returned[0]
        # print(best_guess_returned)
        legal_words = best_guess_returned[1]
        # print(best_guess)
        print(f'{len(legal_words)} possible word(s) remain')
        print(f'The computer reccomends that you play \x1b[3;30;34m{best_guess[0].upper()}\x1b[0m as this provides {best_guess[1]} bits of information.')
    user_guess = get_input()
    pattern = input('What is the pattern of the previous word?\n') if manual_entry else get_pattern(user_guess, answer)
    previous_guess = user_guess
    user_guesses_count += 1
    
    print_word(user_guess, pattern)
    print()

    if all([letter_result == '2' for letter_result in pattern]):
        print(f'congrats, you succeeded with {user_guesses_count} turns')
        break

    if user_guesses_count > 5:
        print(f'sorry you have failed :(\nThe answer was {answer}')
        break
