import pytest

from game_functions import get_pattern
from wordle_engine import is_valid, get_new_list, legal_words


@pytest.mark.parametrize("user_guess, answer, expected_result", [
    ("tarts", 'ultra', '11100'),
    ("farts", 'ultra', '01110'),
    ("crane", 'ultra', '01100'),
    ("oasis", 'ultra', '01000'),
    ("penis", 'ultra', '00000'),
    ("yetis", 'ultra', '00200'),
    ("begin", 'begin', '22222'),
])

def test_pattern(user_guess, answer, expected_result):
    assert get_pattern(user_guess, answer) == expected_result

@pytest.mark.parametrize("word, previous_guess, pattern, expected_result", [
    ("tarts", 'farts', '11100', False),
    ("farts", 'tarps', '01110', False),
    ("light", 'ultra', '01100', True),
    ('abuse', 'penis', '00011', False),
    ("oasis", 'bezel', '00000', True),
    ("yetis", 'ultra', '00200', True),
])

def test_is_valid(word, pattern, previous_guess, expected_result):
    assert is_valid(word, pattern, previous_guess) == expected_result

@pytest.mark.parametrize("guess, answer, expected_result", [
    ("shift", '22022', ['shaft']),
])

def test_get_new_list(guess, answer, expected_result):
    assert get_new_list(guess, answer, legal_words) == expected_result