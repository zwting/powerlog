# -*- coding: utf-8 -*-

class ELogLevel(object):
    LOG = 1
    WARNING = 2
    ERROR = 3

class EConfigKey(object):
    LOG_LEVEL_LIST = "LOG_LEVEL_LIST"

class MainConfig(object):
    _instance = None

    @staticmethod
    def main_config():
        if not MainConfig._instance:
            MainConfig._instance = MainConfig()
        return MainConfig._instance

    def __init__(self):
        self.config = {}

    def add_log_level(self, log_level):
        log_level_list = self.config.setdefault(EConfigKey.LOG_LEVEL_LIST, [])
        if log_level in log_level_list:
            return
        log_level_list.append(log_level)

    def remove_log_level(self, log_level):
        self.config.setdefault(EConfigKey.LOG_LEVEL_LIST, []).remove(log_level)

    def is_has_log_level(self, log_level):
        return log_level in self.config.get(EConfigKey.LOG_LEVEL_LIST, [])

    def save(self):
        pass

    def load(self):
        pass



