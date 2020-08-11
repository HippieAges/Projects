def uses_all(word, required):
    return all(letter in word for letter in required)

print(uses_all("Oleksiy", "Olofmeister"))

def avoids(word, forbidden):
    return set(word).isdisjoint(forbidden)

print(avoids("Oleksiy", "zzzzzzzzz"))

def all_anagrams(filename):
    d = {}
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)
        if t not in d:
            d[t] = [word]
        else:
            d[t].append(word)
    return d

def new_all_anagrams(filename):
    d = {}
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)
        d.setdefault(t, []).append(word)
    return d

from collections import defaultdict

def dict_all_anagrams(filename):
    d = defaultdict(list)
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)
        d[t].append(word)

# chapter 19 exercise 1 <- using conditional expressions
def binomial_coeff(n, k):
    """Compute the binomial coefficient "n choose k".

    n: number of trials
    k: number of successes

    returns: int
    """
    res = 1 if k == 0 else 0 if n == 0 else binomial_coeff(n-1, k) + binomial_coeff(n-1, k-1)

    # res = binomial_coeff(n-1, k) + binomial_coeff(n-1, k-1)
    return res

# print(binomial_coeff(5, 3))

# chapter 19 exercise 1 <- using memoization
known = {}
def memo_binomial_coeff(n, k):

    if (n,k) in known.keys():
        return known[(n,k)]

    if k == 0:
        return known.setdefault((n,k), 1)
    if n == 0:
        return known.setdefault((n,k), 0)

    res = memo_binomial_coeff(n-1, k) + memo_binomial_coeff(n-1, k-1)
    known[(n,k)] = res

    return res

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

# print(memo_binomial_coeff(5, 3))

import timeit

wrapped = wrapper(binomial_coeff, 5, 3)
print("Binomial coefficient with conditional expressions: " + str(timeit.timeit(wrapped)))
wrapped = wrapper(memo_binomial_coeff, 5, 3)
print("Binomial coefficient with the use of memoization: " + str(timeit.timeit(wrapped)))