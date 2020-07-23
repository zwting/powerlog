# -*- coding: utf-8 -*-
import imgui


def set_cursor_offset(offset_x, offset_y):
    pos = imgui.get_cursor_pos()
    imgui.set_cursor_pos((pos[0] + offset_x, pos[1] + offset_y))

def clamp(min, max, val):
    val = min if val < min else val
    val = max if val > max else val
    return val

def get_win_size():
    return imgui.get_style()