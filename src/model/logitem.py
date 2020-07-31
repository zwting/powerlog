# -*- coding: utf-8 -*-
from inspect import getframeinfo


class LogItem(object):
    def __init__(self, stack_info, str):
        self.origin_str = str
        self.frame_info = stack_info
        self.__line_info = None
        self.__stack_info = None

    @property
    def main_msg(self):
        return self.origin_str

    @property
    def line_info(self):
        if not self.__line_info:
            ctx_info = self.stack_info[1]
            self.__line_info = "%s() (at %s:%s)" % (ctx_info[3], ctx_info[1], ctx_info[2])
        return self.__line_info

    @property
    def stack_info(self):
        return
