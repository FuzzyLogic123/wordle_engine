import sys

with open('./data/valid_words.txt') as file:
    valid_entries = [ line.strip() for line in file ]
    
terminal_colours = {
    "green": '\x1b[6;30;42m',
    "grey": '\x1b[6;37;40m',
    "yellow": '\x1b[5;30;43m',
    "red": '\x1b[5;30;41m',
    "end": '\x1b[0m',
}

def delete_lines(n=1):
    "Use this function to delete the last line in the STDOUT"
    for _ in range(n):

        #cursor up one line
        sys.stdout.write('\x1b[1A')

        #delete last line
        sys.stdout.write('\x1b[2K')

def print_coloured(text, colour):
    print(f'{terminal_colours[colour]} {text} {terminal_colours["end"]}', end='')

def print_word(word, pattern):
    for i, number in enumerate(pattern):
        if number == '0':
            colour = "grey"
        elif number == '1':
            colour = "yellow"
        else:
            colour = "green"
        print_coloured(word[i], colour)

def get_pattern(guess, answer):
    """gets the pattern of the guess given the answer. 1 is grey, 2 yellow, 3 green"""
    res = ['', '', '', '', '']
    letters_used = []
    for i in range(len(guess)):
        letter = guess[i]

        if answer[i] == guess[i]:
            res[i] = '2'
            letters_used += [letter]

    for i in range(len(guess)):
        letter = guess[i]
        if letter in answer and not res[i] and letters_used.count(letter) < answer.count(letter):
            res[i] =  '1'
            letters_used += [letter]

    for i in range(len(guess)):
        if not res[i]:
            res[i] = '0'
            
    return ''.join(res)

def get_input():
    user_guess = input()
    delete_lines()

    while len(user_guess) != 5 or user_guess not in valid_entries:
        if len(user_guess) != 5:
            print('guess must be of length 5')
        else:
            print('not a valid English word')
        user_guess = input()
        delete_lines(2)
    return user_guess