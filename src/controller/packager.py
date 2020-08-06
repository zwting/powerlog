# -*- coding: utf-8 -*-
import cPickle
import struct
import time

from src.common import const

def pack(cmd, obj):
    if cmd == const.EPkgType.Cmd:
        data = bytes(obj)
    elif cmd == const.EPkgType.Log:
        ei = obj.exc_info
        if ei:
            obj.exc_info = None  # to avoid Unpickleable error
        d = dict(obj.__dict__)
        d['msg'] = obj.getMessage()
        d['args'] = None
        data = cPickle.dumps(d, 1)
        if ei:
            obj.exc_info = ei  # for next handle
    elif cmd == const.EPkgType.HeartBeat:
        data = bytes(obj)
    if len(data) <= 0:
        return None
    data_cmd = struct.pack(">I", cmd)
    total_data = data_cmd + data
    data_len = struct.pack(">L", len(total_data))
    return data_len + total_data

def unpack(data):
    data_cmd = struct.unpack(">I", data)[0]
