from Pyro4 import expose
import math

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        N = self.read_input()
        limit = int(math.isqrt(N))

        base_primes = self.simple_sieve(limit)

        num_workers = len(self.workers)
        start_val = limit + 1
        total_remaining = N - start_val + 1

        chunk_size = total_remaining // num_workers
        remainder = total_remaining % num_workers

        tasks = []
        curr_start = start_val
        for i in range(num_workers):
            curr_chunk = chunk_size + (1 if i < remainder else 0)
            curr_end = curr_start + curr_chunk - 1
            if curr_start <= curr_end:
                tasks.append(self.workers[i].sieve_range(curr_start, curr_end, base_primes))
            curr_start = curr_end + 1

        all_primes = list(base_primes)
        for res in tasks:
            all_primes.extend(res.value)

        self.write_output(all_primes)

    def simple_sieve(self, limit):
        if limit < 2:
            return []
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for p in range(2, int(math.isqrt(limit)) + 1):
            if sieve[p]:
                for i in range(p * p, limit + 1, p):
                    sieve[i] = False
        return [p for p in range(2, limit + 1) if sieve[p]]

    @staticmethod
    @expose
    def sieve_range(low, high, base_primes):
        length = high - low + 1
        if length <= 0:
            return []

        is_prime = [True] * length

        for p in base_primes:
            first_multiple = max(p * p, ((low + p - 1) // p) * p)
            if first_multiple > high:
                continue
            for mult in range(first_multiple, high + 1, p):
                is_prime[mult - low] = False

        primes = [low + i for i in range(length) if is_prime[i]]
        return primes

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            line = f.readline().strip()
            return int(line)

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            f.write(f"Total primes found: {len(output)}\n")
            f.write(", ".join(map(str, output[:1000])))
            if len(output) > 1000:
                f.write(f"\n... and {len(output) - 1000} more primes.")