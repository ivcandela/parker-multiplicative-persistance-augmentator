from math import floor
from threading import Lock, Thread
from time import time

from solver import Solver
from cache import SolverCache
from permutation import UniqueDigitPermutator
from debug import Debugger
from exceptions import DeadEnd


class ThreadLock:
    def __init__(self):
        self.__threadLock = Lock()

    def acquire(self):
        self.__threadLock.acquire()

    def release(self):
        self.__threadLock.release()


class SolverThread(Thread):
    def __init__(self, thread_id, num_threads, total_permutations, number, debug, file_system):
        Thread.__init__(self)
        self.__thread_id = thread_id
        self.__num_threads = num_threads
        self.__total_permutations = total_permutations
        self.__number = number
        self.__debug = debug
        self.__file_system = file_system

    def run(self):
        debugger = Debugger(full_debug=self.__debug, prefix="Solver#{}".format(self.__thread_id + 1))
        cache = SolverCache(file_system=self.__file_system)
        permutator = UniqueDigitPermutator()

        solver = Solver(cache=cache, permutator=permutator, debugger=debugger)

        total_permutations = self.__total_permutations
        min_permutation = floor(self.__thread_id * total_permutations / self.__num_threads)
        max_permutation = floor((self.__thread_id + 1) * total_permutations / self.__num_threads) - 1

        start_time = time()
        try:
            result = solver.solve(
                self.__number,
                min_permutation=min_permutation,
                max_permutation=max_permutation
            )
            debugger.print("**************", force=True)
            debugger.print("*FINAL RESULT*", force=True)
            debugger.print("**************", force=True)
            debugger.print(result, force=True)
            debugger.print("**************", force=True)
        except DeadEnd:
            debugger.print(":( :( :( :( :(", force=True)
            debugger.print(":(          :(", force=True)
            debugger.print(":(   Nada   :(", force=True)
            debugger.print(":(          :(", force=True)
            debugger.print(":( :( :( :( :(", force=True)
        finally:
            cache.persist()

        execution_time = time() - start_time
        cache_keys_after = cache.keys_count()
        debugger.print(
            '\n - {}s\n - {} cache hits\n - {} cache misses\n - {} cache keys'
                .format(
                    str(execution_time),
                    cache.hit_count(),
                    cache.miss_count(),
                    cache_keys_after
                ),
            force=True
        )
