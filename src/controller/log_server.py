# -*- coding: utf-8 -*-
import logging
import pickle
import select
import socket
import struct
from logging import handlers

from src.common import const
from src.controller import packager
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
        self.write_list = []

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
                    if new_conn not in self.write_list:
                        self.write_list.append(new_conn)
                else:
                    self.read(sock)
        # except socket.error as err:
        except Exception as err:
            print "Exception at", err

    def send(self, str_cmd):
        if not self.socket:
            return
        try:
            rl, wl, el = select.select([], self.write_list, [], 0)
            if not wl:
                return
            data = packager.pack(const.EPkgType.Cmd, str_cmd)
            sender = wl[0]
            if hasattr(sender, "sendall"):
                sender.sendall(data)
            else:
                sent_sofar = 0
                left = len(data)
                while left > 0:
                    sent = sender.send(data[sent_sofar:])
                    sent_sofar += sent
                    left -= sent
        except socket.error:
            sender.close()
            self.write_list.remove(sender)


    def dispatch(self, cmd, data):
        if cmd == const.EPkgType.HeartBeat:
            print ("Heat Beat:", data)
        elif cmd == const.EPkgType.Log:
            obj = pickle.loads(data)
            record = logging.makeLogRecord(obj)
            self.handler.handle(record)
        elif cmd == const.EPkgType.Cmd:
            print ("Cmd: ", data)

    def read(self, sock):
        try:
            chunk = sock.recv(4)
            if chunk <= 0:
                self.read_list.remove(sock)
                self.write_list.remove(sock)
                sock.close()
                return
            if len(chunk) < 4:
               return
            pkg_len = struct.unpack(">L", chunk)[0]
            chunk = sock.recv(pkg_len)
            while len(chunk) < pkg_len:
                chunk += sock.recv(pkg_len - len(chunk))
            cmd = struct.unpack(">I", chunk[0:4])[0]
            self.dispatch(cmd, chunk[4:])

        except socket.error, e:
            if sock != self.socket:
                sock.close()
                self.read_list.remove(sock)
                self.write_list.remove(sock)
            print e
