# -*- coding: utf-8 -*-
import cPickle
import select
import socket
import struct
import threading
import time
from logging import handlers

class EPkgType(object):
    Cmd = 1
    Log = 2
    HeartBeat = 3

def pack(cmd, obj):
    if cmd == EPkgType.Cmd:
        data = bytes(obj)
    elif cmd == EPkgType.Log:
        ei = obj.exc_info
        if ei:
            obj.exc_info = None  # to avoid Unpickleable error
        d = dict(obj.__dict__)
        d['msg'] = obj.getMessage()
        d['args'] = None
        data = cPickle.dumps(d, 1)
        if ei:
            obj.exc_info = ei  # for next handle
    elif cmd == EPkgType.HeartBeat:
        data = bytes(obj)
    if len(data) <= 0:
        return None
    data_cmd = struct.pack(">I", cmd)
    total_data = data_cmd + data
    data_len = struct.pack(">L", len(total_data))
    return data_len + total_data

class PowerLogSockHandler(handlers.SocketHandler):
    def __init__(self, host, port, remote_cmd_handler, timeout=0.05, hb_duration=8):
        super(PowerLogSockHandler, self).__init__(host, port)
        self.timeout = timeout
        self.remote_cmd_handler = remote_cmd_handler
        self.read_list = []
        self.last_hb_time = None
        self.hb_duration = hb_duration

    def try_receive(self):
        try:
            if not self.read_list:
                self.sock = self.makeSocket()
            if not self.read_list:
                return
            rl, wl, el = select.select(self.read_list, self.read_list, [], 0)
            if time.time() - self.last_hb_time >= self.hb_duration and wl:
                self.last_hb_time = time.time()
                send_data = pack(EPkgType.HeartBeat, self.last_hb_time)
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
        except socket.error as socket_err:
            import errno
            print "[1]socket.error: %s" % socket_err
            self.read_list = []
            self.sock = None
        except select.error as select_err:
            print "[2]select.error: %s" % select_err

    def makeSocket(self, timeout=1.0/60):
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if hasattr(sock, 'settimeout'):
                sock.settimeout(timeout)
            errno = sock.connect_ex((self.host, self.port))
            if errno != 0:
                return None
            self.last_hb_time = 0
            self.read_list = []
            self.read_list.append(sock)
            return sock
        except socket.error as socket_err:
            print "[3]socket.error：%s" % socket_err
            # print errno.errorcode[err[1]]


    def makePickle(self, record):
        return pack(EPkgType.Log, record)
