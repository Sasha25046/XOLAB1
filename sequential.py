import math
import time


def simple_sieve(limit):
    if limit < 2:
        return []

    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0

    max_p = int(math.floor(math.sqrt(limit)))

    for p in range(2, max_p + 1):
        if sieve[p]:
            for i in range(p * p, limit + 1, p):
                sieve[i] = 0

    return [p for p in range(2, limit + 1) if sieve[p]]


def sequential_sieve(N):

    if N < 2:
        return []

    limit = int(math.floor(math.sqrt(N)))

    base_primes = simple_sieve(limit)

    start = limit + 1
    length = N - start + 1

    is_prime = bytearray([1]) * length

    for p in base_primes:


        first_multiple = max(
            p * p,
            ((start + p - 1) // p) * p
        )

        if first_multiple > N:
            continue

        for multiple in range(first_multiple, N + 1, p):
            is_prime[multiple - start] = 0

    remaining_primes = [
        start + i
        for i in range(length)
        if is_prime[i]
    ]

    return base_primes + remaining_primes


def main():


    N = 100000000

    print("=" * 60)
    print("Послідовний алгоритм — решето Ератосфена")
    print("=" * 60)
    print("N =", N)
    print()

    start_time = time.perf_counter()

    primes = sequential_sieve(N)

    end_time = time.perf_counter()

    duration = end_time - start_time

 
    print("=" * 60)
    print("Total primes found:", len(primes))
    print("Pure sequential time (T_seq): {:.2f} s".format(duration))
    print("=" * 60)


    print("Запис результату у sequential_output.txt...")

    with open("sequential_output.txt", "w", buffering=2*1024*1024) as f:
        f.write("Range: 1 to %d\n" % N)
        f.write("Total primes found: %d\n\n" % len(primes))
        f.write("Primes list:\n")

        batch_size = 50000
        total_len = len(primes)
        for i in range(0, total_len, batch_size):
            chunk = "\n".join(str(p) for p in primes[i:i + batch_size]) + "\n"
            f.write(chunk)

    print("Result successfully saved to sequential_output.txt")


if __name__ == "__main__":
    main()