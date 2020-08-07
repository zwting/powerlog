# -*- coding: utf-8 -*-
import cPickle
import select
import struct
import time
from logging import handlers

from src.common import const
from src.controller import packager


class PowerLogSockHandler(handlers.SocketHandler):
    def __init__(self, host, port, remote_cmd_handler, timeout=15, hb_duration=8):
        super(PowerLogSockHandler, self).__init__(host, port)
        self.timeout = timeout
        self.remote_cmd_handler = remote_cmd_handler
        self.read_list = []
        self.last_hb_time = None
        self.hb_duration = hb_duration

    def try_receive(self):
        if not self.sock:
            return
        try:
            rl, wl, el = select.select(self.read_list, self.read_list, [], 0)
            if time.time() - self.last_hb_time >= self.hb_duration and wl:
                self.last_hb_time = time.time()
                send_data = packager.pack(const.EPkgType.HeartBeat, self.last_hb_time)
                self.send(send_data)

            if not rl:
                return
            chunk = rl[0].recv(4)
            if len(chunk) < 4:
                return
            pkg_len = struct.unpack(">L", chunk)[0]
            chunk = rl[0].recv(pkg_len)
            while len(chunk) < pkg_len:
                chunk += rl[0].recv(pkg_len - len(chunk))
            cmd = struct.unpack(">I", chunk[0:4])
            self.remote_cmd_handler(str(chunk[4:]))
        except Exception as e:
            self.sock = self.makeSocket()
            print e

    def makeSocket(self):
        socket = super(PowerLogSockHandler, self).makeSocket(self.timeout)
        self.last_hb_time = 0
        self.read_list = []
        self.read_list.append(socket)
        return socket

    def makePickle(self, record):
        return packager.pack(const.EPkgType.Log, record)
