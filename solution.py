# -*- coding: utf-8 -*-
from Pyro4 import expose
import math

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        N = self.read_input()
        limit = int(math.floor(math.sqrt(N)))

        base_primes = self.simple_sieve(limit)

        num_workers = len(self.workers)
        start_val = limit + 1
        total_remaining = N - start_val + 1

        chunk_size = total_remaining // num_workers
        remainder = total_remaining % num_workers

        tasks = []
        curr_start = start_val
        for i in xrange(num_workers):
            curr_chunk = chunk_size + (1 if i < remainder else 0)
            curr_end = curr_start + curr_chunk - 1
            if curr_start <= curr_end:
                tasks.append(self.workers[i].sieve_primes(curr_start, curr_end, base_primes))
            curr_start = curr_end + 1

        worker_results = [res.value for res in tasks]

        total_primes = len(base_primes) + sum(count for count, _ in worker_results)

        with open(self.output_file_name, 'w') as f:
            f.write("Range: 1 to %d\n" % N)
            f.write("Total primes found: %d\n\n" % total_primes)
            f.write("Primes list:\n")
            if base_primes:
                f.write("\n".join(str(p) for p in base_primes) + "\n")
            for _, primes_text in worker_results:
                f.write(primes_text)

    def simple_sieve(self, limit):
        if limit < 2:
            return []
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        max_p = int(math.floor(math.sqrt(limit)))
        for p in xrange(2, max_p + 1):
            if sieve[p]:
                for i in xrange(p * p, limit + 1, p):
                    sieve[i] = False
        return [p for p in xrange(2, limit + 1) if sieve[p]]

    @staticmethod
    @expose
    def sieve_primes(low, high, base_primes):
        length = high - low + 1
        if length <= 0:
            return (0, "")

        is_prime = bytearray([1]) * length

        for p in base_primes:
            first_multiple = max(p * p, ((low + p - 1) // p) * p)
            if first_multiple > high:
                continue
            for mult in xrange(first_multiple, high + 1, p):
                is_prime[mult - low] = 0

        primes = [str(low + i) for i in xrange(length) if is_prime[i]]
        return (len(primes), "\n".join(primes) + "\n")

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            line = f.readline().strip()
            return int(line)
