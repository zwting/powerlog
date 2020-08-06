# -*- coding: utf-8 -*-
import logging
import pickle
import select
import socket
import struct
from logging import handlers

from src.controller.log_mgr import LogMgr


class PowerLogHandler(logging.Handler):
    def __init__(self):
        # self.app = app
        pass

    def handle(self, record):
        LogMgr.instance().push_log(record)


class LogServer(object):
    def __init__(self, handler, host="localhost", port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        self.host = host
        self.port = port
        self.handler = handler
        self.socket = None

        logging.getLogger('').setLevel(logging.DEBUG)
        logging.basicConfig(
            format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')

        self.init_socket()

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def receive(self):
        try:
            rl, wl, el = select.select([self.socket], [], [], 0)
            if not rl:
                return
            conn, addr = rl[0].accept()
            chunk = conn.recv(4)
            if len(chunk) < 4:
                conn.close()
                return
            pkg_len = struct .unpack(">L", chunk)[0]
            chunk = conn.recv(pkg_len)
            while len(chunk) < pkg_len:
                chunk += conn.recv(pkg_len - len(chunk))
            obj = pickle.loads(chunk)
            record = logging.makeLogRecord(obj)
            self.handler.handle(record)
            conn.close()
        except socket.error as err:
            conn and conn.close()
            print err
