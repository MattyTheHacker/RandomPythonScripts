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



def remove_duplicates_from_list(input_list):
    return list(set(input_list))


def find_all_pairs_that_sum_to_x(list, x):
    pairs = []
    for i in range(len(list)):
        for j in range(i+1, len(list)):
            if list[i] + list[j] == x:
                pairs.append((list[i], list[j]))
    return pairs


def find_unique_pairs_that_sum_to_x(list, x):
    pairs = []
    for i in range(len(list)):
        for j in range(i+1, len(list)):
            if list[i] + list[j] == x:
                pairs.append((list[i], list[j]))
    return set(pairs)


def is_palindrome(string):
    if string == string[::-1]:
        return True
    return False


def intersection_of_lists(list_one, list_two):
    return list(set(list_one) & set(list_two))


def union_of_lists(list_one, list_two):
    return list(set(list_one) | set(list_two))


def difference_of_lists(list_one, list_two):
    return list(set(list_one) - set(list_two))


def check_if_list_is_subset_of_another_list(list_one, list_two):
    if set(list_one).issubset(set(list_two)):
        return True
    return False


def reverse_string(string):
    return string[::-1]



def reverse_string_recursive(string):
    if len(string) == 1:
        return string
    return string[-1] + reverse_string_recursive(string[:-1])


def reverse_string_iterative(string):
    reversed_string = ""
    for i in range(len(string)):
        reversed_string += string[-i-1]
    return reversed_string


def find_fibonacci_number(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return find_fibonacci_number(n-1) + find_fibonacci_number(n-2)



