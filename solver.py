import math

from exceptions import DeadEnd


class Solver:
    def __init__(self, cache, permutator, debugger):
        self.__cache = cache
        self.__permutator = permutator
        self.__debugger = debugger

        cache.read_from_persisted()

    def solve(self, number, min_permutation=0, max_permutation=float("inf")):
        self.__debugger.print(
            '///////////////////////////// solving {} from {} to {}'.format(number, min_permutation, max_permutation),
            force=True)

        permutation_counter = 0

        for p in self.__permutator.get_next_permutation(number):

            if permutation_counter > max_permutation:
                break

            permutation_counter += 1

            if permutation_counter < min_permutation:
                continue

            if not self.__cache.check(p):
                self.__cache.persist()

            done_in_tranche = permutation_counter - min_permutation
            tranche_size = max_permutation - min_permutation
            progress = done_in_tranche / tranche_size
            self.__debugger.print(" *** {} - permutation n.{}/{} ({}/{} or {}% of tranche)".format(
                p,
                permutation_counter,
                max_permutation,
                done_in_tranche,
                tranche_size,
                round(progress * 100, 2)
            ), force=True)
            try:
                result = self.__try_to_find_single_digit_divisors(p)
                return int("".join(sorted(result)))
            except DeadEnd:
                self.__debugger.print(" *** deadend permutation", p)
                continue
        raise DeadEnd()

    def __try_to_find_single_digit_divisors(self, n):
        self.__debugger.print("n", n)

        if self.__cache.check(n):
            try:
                self.__debugger.print("CACHE HIT", n)
                return self.__cache.get(n)
            except DeadEnd:
                self.__debugger.print("CACHE HIT -> DEADEND", n)
                raise DeadEnd()

        if n < 10:
            self.__debugger.print("n < 10, returning")
            result = [str(n)]
            self.__cache.store(n, result)
            return result

        i = 1
        while i < math.ceil(math.sqrt(n)):
            i += 1

            self.__debugger.print(" ---- i", i, n)
            if n % i != 0:
                continue

            self.__debugger.print(" --- divisor found", i, n)
            try:
                result = self.__try_to_find_single_digit_divisors(i) + self.__try_to_find_single_digit_divisors(
                    int(n / i))
                self.__debugger.print("result", "".join(result), n)
                self.__cache.store(n, result)
                return result
            except DeadEnd:
                self.__debugger.print(" ------- i is a deadend", i, n)
                continue

        self.__cache.deadend(n)
        raise DeadEnd()
