from functools import reduce
from collections import defaultdict as dd
import timeit


def primes_imperative(n):
    """
    Takes `n` - a natural number - as an input.
    Returns a list of prime numbers up to `n` inclusively.
    These primes are found using the Sieve of Eratosthenes.
    """

    result = []

    # no primes lower than 2
    if n < 2:
        return result

    isprime = [True for _ in range(n + 1)]  # declaring an array which informs if a number (as index) is prime or not
    isprime[1] = False

    # all even natural numbers except 2 are not primes
    for i in range(0, n + 1, 2):
        isprime[i] = False

    isprime[2] = True
    result.append(2)

    # sieving odd natural numbers (even numbers are already sieved)
    for i in range(3, n + 1, 2):
        if isprime[i]:
            result.append(i)

            k = 3 * i  # starting from 3i, because 2i is even and it has been sieved out before
            while k <= n:
                isprime[k] = False  # k is a multiple of some smaller number larger than one
                k += 2 * i  # stepping by 2i because it ensures landing on an odd number

    return result

# 'lcomp' stands for 'list comprehension'
def primes_lcomp(n):
    """
    Takes `n` - a natural number - as an input.
    Returns a list of prime numbers up to `n` inclusively.
    These primes `i` are found by checking if a list of positive natural divisors of `i`,
    different than `1` and `i`, is empty.
    """

    # complexity: for every `i` it takes O(sqrt(i)) to process `i`
    return [i for i in range(2, n + 1) if not [k for k in range(2, int(i ** 0.5) + 1) if i % k == 0]]

def primes_functional1(n):
    """
    Takes `n` - a natural number - as an input.
    Returns a list of prime numbers up to `n` inclusively.
    These primes `i` are found by checking if all numbers inclusively
    between `2` and `floor(i ** 0.5)` are not divisors of `i`.
    """

    # complexity: for every `i` it takes O(sqrt(i)) to process `i`
    return list(filter(lambda i: all(i % k for k in range(2, int(i ** 0.5) + 1)), range(2, n + 1)))

def primes_functional2(n):
    """
    Takes `n` - a natural number - as an input.
    Returns a list of prime numbers up to `n` inclusively.
    Numbers inclusively from range `2` to `n` are processed in a foldr manner.
    In the process, prime numbers up to the current number exclusively have been found.
    If the current number is not divisible by any prime smaller than it, then the current number
    is a prime as well and therefore is added to the list of primes found, else nothing is added
    to it.
    """

    # complexity: for every `i` it takes O([number of primes up to `i`]) to process `i`
    return list(reduce(lambda primes, i: primes + ([i] if all(i % p for p in primes) else []),
                       range(2, n + 1),
                       []))


print(primes_imperative(1))
print(primes_lcomp(1))
print(primes_functional1(1))
print(primes_functional2(1))

print(primes_imperative(2))
print(primes_lcomp(2))
print(primes_functional1(2))
print(primes_functional2(2))

print(primes_imperative(50))
print(primes_lcomp(50))
print(primes_functional1(50))
print(primes_functional2(50))

print(primes_imperative(100))
print(primes_lcomp(100))
print(primes_functional1(100))
print(primes_functional2(100))

i = 100000
print(timeit.timeit(lambda: primes_imperative(i), number=1))
print(timeit.timeit(lambda: primes_lcomp(i), number=1))
print(timeit.timeit(lambda: primes_functional1(i), number=1))
print(timeit.timeit(lambda: primes_functional2(i), number=1))
print()

relative_performance = dd(float)
N = 14
for i in range(1, N + 1):
    test = 50 * i

    imp   = timeit.timeit(lambda: primes_imperative(test), number=1000)
    lcomp = timeit.timeit(lambda: primes_lcomp(test), number=1000)
    func1 = timeit.timeit(lambda: primes_functional1(test), number=1000)
    func2 = timeit.timeit(lambda: primes_functional2(test), number=1000)

    best = min(imp, lcomp, func1, func2)


    # storing the sum of the quotients of performance compared to the best performance
    relative_performance['imperative']    += imp / best
    relative_performance['list comp']     += lcomp / best
    relative_performance['functional 1.'] += func1 / best
    relative_performance['functional 2.'] += func2 / best

    # the quotients tend to increase with `test`, but that's expected
    # since the best solution (imperative Sieve of Eratosthenes)
    # has lower asymptotic time complexity than the rest
    # therefore the execution time of the rest grows faster than imperative's
    print(f'relative performance to the best one (test = {test}):')
    print('imperative:\t', imp / best)
    print('list comp:\t', lcomp / best)
    print('functional 1.:\t', func1 / best)
    print('functional 2.:\t', func2 / best)
    print()


# the conclusion is that the imperative implementation of the Sieve of Eratosthenes
# is the fastest solution among those implemented above
print()
print(f'relative performance to the best one on average (for {N} different tests):')
for version, performance in relative_performance.items():
    print('\t' + version + ':\t', performance / N)
