from sympy import factorint

# is prime
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if not(n & 1):
        return False
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False
    return True

# next prime
def next_prime(n):
    if n < 2:
        return 2
    if n == 2:
        return 3
    if not(n & 1):
        n += 1
    else:
        n += 2
    while not is_prime(n):
        n += 2
    return n

# prime factorization for n
def prime_factors(n):
    #checks if n is even which means 2 is one of the prime factors
    if not(n & 1):
        # returns 2 and n // 2
        return (2, n >> 1)
    i = 3
    while n % i != 0:
        i += 2
    return (i, n // i)

# prime factorization for n built-in
def prime_factors_builtin(n):
    # Use factorint() method
    factor_dict = factorint(n)
    list_primes = tuple(factor_dict.keys())
    return list_primes
