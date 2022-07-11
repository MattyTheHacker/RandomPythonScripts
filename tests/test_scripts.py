from scripts.interviewquestions import *

def test_check_if_list_contains_int():
    numbers = [1, 2, 3, 4, 5]
    for number in numbers:
        assert check_if_list_contains_int(numbers, number) == True


def test_intersection_of_lists():
    list_one = [1, 2, 3, 4, 5]
    list_two = [4, 5, 6, 7, 8]
    assert intersection_of_lists(list_one, list_two) == [4, 5]

def test_union_of_lists():
    list_one = [1, 2, 3, 4, 5]
    list_two = [4, 5, 6, 7, 8]
    assert union_of_lists(list_one, list_two) == [1, 2, 3, 4, 5, 6, 7, 8]


def test_check_if_two_strings_are_anagrams():
    string_one = "bad"
    string_two = "dab"
    assert check_if_two_strings_are_anagrams(string_one, string_two) == True
    string_one = "debit card"
    string_two = "bad credit"
    assert check_if_two_strings_are_anagrams(string_one, string_two) == True
    string_one = "random string"
    string_two = "another random string"
    assert check_if_two_strings_are_anagrams(string_one, string_two) == False





