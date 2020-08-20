# -*- coding: utf-8 -*-
import logging
from collections import deque

class LoggerWrap(object):
    def __init__(self, log_record):
        self.log_record = log_record
        self.detail_formatter = None

    @property
    def msg_with_level(self):
        return "[%s] %s" % (self.log_record.levelname, str(self.log_record.msg))

    @property
    def file_info(self):
        return "(%s:%d)" % (self.log_record.pathname, self.log_record.lineno)

    @property
    def detail_info(self):
        if not self.detail_formatter:
            self.detail_formatter = \
                logging.Formatter(fmt='[%(levelname)s][%(asctime)s] (%(pathname)s:%(lineno)d) in %(funcName)s()\n%(message)s')
        return self.detail_formatter.format(self.log_record)

    @property
    def msg(self):
        return self.log_record.msg

    @property
    def filename(self):
        return self.log_record.filename

    @property
    def create_time_in_str(self):
        return str(self.log_record.created)

    @property
    def level(self):
        return self.log_record.levelno

class LogMgr(object):
    _instance = None

    @staticmethod
    def instance():
        if LogMgr._instance:
            return LogMgr._instance
        LogMgr._instance = LogMgr()
        return LogMgr._instance

    def __init__(self):
        self.max_log_count = 5000
        self.log_lst = deque(maxlen=self.max_log_count)

    @property
    def main_view(self):
        from src.controller.app import App
        ins = App.instance()
        return ins and ins.main_view

    def push_log(self, log_record):
        self.log_lst.append(LoggerWrap(log_record))

    def clear(self):
        self.log_lst.clear()