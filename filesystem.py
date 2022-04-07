import json
import os
import shutil
import time


class JsonFileSystem:
    def __init__(self, file_path, lock):
        self.__file_path = file_path
        self.__lock = lock

    def read_json(self):
        self.__lock.acquire()
        try:
            return self.__actually_read()
        finally:
            self.__lock.release()

    def read_and_write_json(self, json_data):
        self.__lock.acquire()
        data = self.__actually_read() | json_data
        self.__actually_write(data)
        self.__lock.release()
        return data

    def backup(self):
        self.__lock.acquire()
        shutil.copyfile(self.__get_file_path(), self.__get_file_path()+'.'+str(time.time()))
        self.__lock.release()

    def __actually_write(self, json_data):
        with open(self.__get_file_path(), 'w') as file:
            file.write(json.dumps(json_data))

    def __actually_read(self):
        if not os.path.exists(self.__get_file_path()):
            return {}
        try:
            with open(self.__get_file_path(), 'r') as file:
                return json.load(file)
        except json.decoder.JSONDecodeError:
            return {}

    def __get_file_path(self):
        return self.__file_path
