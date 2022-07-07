def check_if_list_contains_int(list_of_ints, int_to_check):
    if int_to_check in list_of_ints:
        return True
    return False


def find_first_duplicate_int_in_list(list_of_ints):
    for i in range(len(list_of_ints)):
        if list_of_ints[i] in list_of_ints[i+1:]:
            return list_of_ints[i]
    return None


def find_all_duplicates_int_in_list(list_of_ints):
    duplicates = [
        number for number in list_of_ints if list_of_ints.count(number) > 1]
    unique_duplicates = list(set(duplicates))
    return unique_duplicates


def check_if_two_strings_are_anagrams(string_one, string_two):
    if len(string_one) != len(string_two):
        return False
    if(sorted(string_one) == sorted(string_two)):
        return True
    return False


















# Testing
numbers = [1, 2, 3, 2, 5, 3, 3, 5, 6, 3, 4, 5, 7]
print(find_first_duplicate_int_in_list(numbers))
print(find_all_duplicates_int_in_list(numbers))
print(check_if_list_contains_int(numbers, 3))
print(check_if_two_strings_are_anagrams("abc", "cba"))



