# -*- coding: utf-8 -*-
import logging
import sys
from StringIO import StringIO


class MyIO(StringIO):
    def __init__(self):
        pass

    def write(self, s):
        logging.info(s + str(ord(s[-1])))


sys.stdout = MyIO()

logging.basicConfig(filename="example.log", filemode='w', level=logging.DEBUG)

print "abc", "zwt", "lt", "haha"