from datetime import datetime


class Debugger:
    def __init__(self, prefix="Debug", full_debug=False):
        self.__full_debug = full_debug
        self.__prefix = prefix

    def print(self, *args, force=False):
        if force or self.__full_debug:
            print(datetime.now(), self.__prefix, *args)
