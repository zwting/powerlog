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
        logger = logging.getLogger('')
        logger.handle(record)


class LogServer(object):
    def __init__(self, handler, host="localhost", port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        self.host = host
        self.port = port
        self.handler = handler
        self.socket = None
        self.read_list = []

        logging.getLogger('').setLevel(logging.DEBUG)
        logging.basicConfig(
            format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')

        self.init_socket()

    def init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.read_list.append(self.socket)

    def receive(self):
        try:
            rl, wl, el = select.select(self.read_list, [], [], 0)
            if not rl:
                return

            for sock in rl:
                if sock is self.socket:
                    new_conn, addr = sock.accept()
                    self.read_list.append(new_conn)
                    self.read(new_conn)
                else:
                    self.read(sock)
        # except socket.error as err:
        except Exception as err:
            print "Exception at", err

    def read(self, sock):
        try:
            chunk = sock.recv(4)
            if chunk <= 0:
                self.read_list.remove(sock)
                sock.close()
                return
            if len(chunk) < 4:
               return
            pkg_len = struct.unpack(">L", chunk)[0]
            chunk = sock.recv(pkg_len)
            while len(chunk) < pkg_len:
                chunk += sock.recv(pkg_len - len(chunk))
            obj = pickle.loads(chunk)
            record = logging.makeLogRecord(obj)
            self.handler.handle(record)
        except socket.error, e:
            if sock != self.socket:
                sock.close()
                self.read_list.remove(sock)
            print e
