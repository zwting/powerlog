# -*- coding: utf-8 -*-
import imgui

key_down_prev_map = {}
key_down_map = {}

def set_cursor_offset(offset_x, offset_y):
    pos = imgui.get_cursor_pos()
    imgui.set_cursor_pos((pos[0] + offset_x, pos[1] + offset_y))

def clamp(min, max, val):
    val = min if val < min else val
    val = max if val > max else val
    return val

def get_win_size():
    return imgui.get_style()

def set_style_color(color_id, color):
    style = imgui.get_style()
    if not style:
        return
    old_color = style.colors[color_id]
    if isinstance(color, imgui.Vec4):
        style.colors[color_id] = color
    elif isinstance(color, tuple):
        style.colors[color_id] = imgui.Vec4(color[0], color[1], color[2], color[3])
    return old_color

def hex_2_vec4(hex_color):
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]
    if len(hex_color) == 3:
        hex_color = hex_color[0] * 2 + hex_color[1] * 2 + hex_color[2] * 2
    return imgui.Vec4(int(hex_color[0:2], 16) / 255.0,
                      int(hex_color[2:4], 16) / 255.0,
                      int(hex_color[4:6], 16) / 255.0,
                      1
                      )

def is_menu_item_click(str_label, str_shortcut=None, bool_selected=False, enabled=True):
    ret = imgui.menu_item(str_label, str_shortcut, bool_selected, enabled)
    return ret[0]

# 过滤搜索结果
def filter_search_text(search_text, record):
    if not search_text:
        return True
    "".startswith("f:")
    len_text = len(search_text)
    if len_text > 2 and search_text.startswith("f:"):
        real_key = search_text[2:]
        print real_key
        if not real_key:
            return True
        return real_key in record.filename[:-3]
    else:
        if len_text == 2:
            return True
        return search_text in record.msg
