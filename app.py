from cache import SolverCache
from filesystem import JsonFileSystem
from permutation import UniqueDigitPermutator
from constants import NUMBER_TO_BEAT, DEFAULT_TOTAL_PERMUTATIONS
from thread import ThreadLock, SolverThread


class SolverApp:
    def run(self, number, debug, num_threads, file_path):
        print("* Adding 1 to the multiplicative persistence of {} *".format(number))

        file_system = JsonFileSystem(file_path=file_path, lock=ThreadLock())
        cache = SolverCache(file_system=file_system)
        cache.backup()

        total_permutations = self.__get_total_permutations(number)

        threads = []
        for thread_id in range(0, num_threads):
            threads.append(
                SolverThread(
                    thread_id=thread_id,
                    num_threads=num_threads,
                    total_permutations=total_permutations,
                    number=number,
                    debug=debug,
                    file_system=file_system
                )
            )

        for thread in threads:
            thread.start()

    @staticmethod
    def __get_total_permutations(number):
        if number == NUMBER_TO_BEAT:
            return DEFAULT_TOTAL_PERMUTATIONS
        return UniqueDigitPermutator().get_count(number)
