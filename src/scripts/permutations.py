import functools
import itertools
import operator
from string import ascii_lowercase


def itertools_permuations_example():
    n, r = 5, 5
    for permuation in itertools.permutations(range(n), r):
        print(permuation)


def itertools_permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def count_permutations(n, r):
    if r > n:
        return 0
    if r < 0:
        raise ValueError('r must be a positive integer.')
    return functools.reduce(operator.mul, range(n - r + 1, n + 1))


def _permutations_recursive(items, i, r):
    if r == 1:
        yield
        return

    for j in range(i, len(items)):
        items[i], items[j] = items[j], items[i]
        yield from _permutations_recursive(items, i + 1, r - 1)

    items.append(items.pop(i))


def permutations_recursive(iterable, r=None):
    items = tuple(iterable)
    n = len(items)
    r = n if r is None else r
    if r > n:
        return
    if r < 0:
        raise ValueError('r must be a positive integer.')
    indices = list(range(n))

    for _ in _permutations_recursive(indices, 0, r):
        yield tuple(items[indices[i]] for i in range(r))


def swap_msg(i, j, n):
    return '|'.join(''.join(['i' if i == x else '', 'j' if j == x else '', ' ' if x not in [i, j] else '']) for x in range(n) + f'Swapping {i} and {j}')


def push_to_back_msg(i, n):
    return '|'.join(''.join(['x' if i == x else '', 'i' if x == n - 1 else '', ' ' if x not in [i, n - 1] else '']) for x in range(n)) + f'Pushing {i} to back'


def countdown(n, r):
    ticks = list(range(n, n - r, -1))
    while True:
        for i in reversed(range(r)):
            ticks[i] -= 1
            yield i, ticks
            if ticks[i] == 0:
                ticks[i] = n - i
            else:
                break
        else:
            return


def _permutations_iterative_with_stack(items, r0):
    n = len(items)
    stack = [(0, r0, 0)]
    while stack:
        i, r, j = stack.pop()
        if r == 0:
            yield
        elif j < n:
            items[i], items[j] = items[j], items[i]
            stack.append((i, r, j + 1))
            stack.append((i + 1, r - 1, i + 1))
        elif j == n:
            items.append(items.pop(i))
        else:
            raise RuntimeError(
                'This is the one thing we *didn\'t* want to happen.')


def _permutations_iterative_no_stack(items, r0):
    n = len(items)
    yield
    for i, ticks in countdown(n, r0):
        tick = ticks[i]
        if tick == 0:
            items.append(items.pop(i))
        else:
            j = n - tick
            items[i], items[j] = items[j], items[i]
            yield


def permutations_iterative(iterable, r=None):
    items = tuple(iterable)
    n = len(items)
    r = n if r is None else r
    if r > n:
        return
    if r < 0:
        raise ValueError('r must be a positive integer.')
    indices = list(range(n))
    for _ in _permutations_iterative_no_stack(indices, r):
        yield tuple(items[indices[i]] for i in range(r))


def main():
    # Testing it all!
    N = 6

    for n, r in itertools.product(range(N), range(N + 1)):
        items = ascii_lowercase[:n]
        expected = list(itertools.permutations(items, r))
        actual_recursive = list(permutations_recursive(items, r))
        assert actual_recursive == expected, (actual_recursive, expected)

        actual_iterative = list(permutations_iterative(items, r))
        assert actual_iterative == expected, (actual_iterative, expected)

        assert count_permutations(n, r) == len(
            expected), (count_permutations(n, r), len(expected))


if __name__ == '__main__':
    main()
