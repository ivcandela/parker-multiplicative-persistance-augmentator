from exceptions import DeadEnd


class SolverCache:
    def __init__(self, file_system):
        self.__file_system = file_system

        self.__cache = {}
        self.__hits = 0
        self.__misses = 0

        self.__DEADEND = -1

    def check(self, key):
        hit = str(key) in self.__cache
        if hit:
            self.__hits += 1
        else:
            self.__misses += 1
        return hit

    def get(self, key):
        key = str(key)
        if self.__cache[key] == self.__DEADEND:
            raise DeadEnd()
        return self.__cache[key]

    def store(self, key, value):
        self.__cache[str(key)] = value

    def deadend(self, key):
        self.store(key, self.__DEADEND)

    def read_from_persisted(self):
        self.__cache = self.__cache | self.__file_system.read_json()

    def persist(self):
        self.__cache = self.__cache | self.__file_system.read_and_write_json(self.__cache)

    def backup(self):
        self.__file_system.backup()

    def hit_count(self):
        return self.__hits

    def miss_count(self):
        return self.__misses

    def keys_count(self):
        return len(self.__cache)
