import timeit
from collections import defaultdict as dd


"""
Functions below include an optimization to check divisors only up to `floor(sqrt(i))`.
If `k` is less than or equal to `floor(sqrt(i))` and divides `i`,
then there exists a divisor of `i`, namely `k' = i // k`, that's larger than or equal to `floor(sqrt(i))`.
However, to make the program not double-count a divisor `k` into the sum (when `k` is exactly `floor(sqrt(i))`),
the code needs to get a bit uglier.

Also, since `1` divides any natural number, it is added to the sum of divisors before
looking for other divisors. `1` is excluded from checking if it divides `i`, because
it always does, and if it was checked, then `i` itself would be added to the sum (`i / 1` equals `i`),
and in that situation the whole sum should be tested against `2 * i`.

`1` is omitted when looking for perfect numbers, because this is an edge case for the described optimization.
It's known that `1` is not a perfect number, and that fact is easily checkable,
so that's why I allowed myself to omit `1`.

Complexity of the whole solution: for every `i` it takes O(`sqrt(i)`) to process `i`.
"""

def perfect_imperative(n):
    """
    Takes `n` - a natural number - as an input.
    Finds all perfect numbers up to `n` inclusively
    by straightforwardly checking the perfection of
    every number inclusively between `2` and `n`.
    """

    perfects = []

    for i in range(2, n + 1):
        s = 1  # accumulator for the sum of divisors

        for k in range(2, int(i ** 0.5) + 1):  # looking for divisors
            if i % k == 0:
                # adding adequate number to the sum

                # this step is described in the multiline comment
                # at the top of the file
                s += k + (i // k if i // k != k else 0)
        
        # condition of perfection
        if s == i:
            perfects.append(i)

    return perfects

# 'lcomp' stands for 'list comprehension'
def perfect_lcomp(n):
    """
    Takes `n` - a natural number - as an input.
    Finds all perfect numbers up to `n` inclusively
    by straightforwardly checking the perfection of
    every number inclusively between `2` and `n`.
    """

    # code without an optimization described above
    # return [i for i in range(1, n + 1) if i == sum([k for k in range(1, i) if i % k == 0])]

    return [i for i in range(2, n + 1) if i == 1 + sum([k + (i // k if i // k != k else 0) for k in range(2, int(i ** 0.5) + 1) if i % k == 0])]

def perfect_functional(n):
    """
    Takes `n` - a natural number - as an input.
    Finds all perfect numbers up to `n` inclusively
    by straightforwardly checking the perfection of
    every number inclusively between `2` and `n`.
    """

    # code without an optimization described above
    # return list(filter(lambda i: i == sum(k for k in range(1, i) if i % k == 0), range(1, n + 1)))

    # the version immediately below is significantly slower
    # return list(filter(lambda i: i == sum(filter(lambda k: i % k == 0, range(1, i))), range(1, n + 1)))

    return list(filter(lambda i: i == 1 + sum(k + (i // k if i // k != k else 0) for k in range(2, int(i ** 0.5) + 1) if i % k == 0), range(2, n + 1)))


print(perfect_imperative(100000))
print(perfect_lcomp(100000))
print(perfect_functional(100000))
print()

print("tested 100 times for n = 10000:")
print("imperative:\t", timeit.timeit(lambda: perfect_imperative(10000), number=100))
print("list comp:\t", timeit.timeit(lambda: perfect_lcomp(10000), number=100))
print("functional:\t", timeit.timeit(lambda: perfect_functional(10000), number=100))
print()

relative_performance = dd(float)
N = 50
for i in range(1, N + 1):
    test = 100 * i

    imp   = timeit.timeit(lambda: perfect_imperative(test), number=100)
    lcomp = timeit.timeit(lambda: perfect_lcomp(test), number=100)
    func  = timeit.timeit(lambda: perfect_functional(test), number=100)

    best = min(imp, lcomp, func)


    # storing the sum of the quotients of performance compared to the best performance
    relative_performance['imperative'] += imp / best
    relative_performance['list comp']  += lcomp / best
    relative_performance['functional'] += func / best

    print(f'relative performance to the best one (test = {test}):')
    print('imperative:\t', imp / best)
    print('list comp:\t', lcomp / best)
    print('functional:\t', func / best)
    print()


# results tell that every solution is approximately the same time complexity
# since quotients remain roughly the same throughout different test cases

# the fastest among them is imperative, and the slowest is functional
print()
print(f'relative performance to the best one on average (for {N} different tests):')
for version, performance in relative_performance.items():
    print('\t' + version + ':\t', performance / N)
