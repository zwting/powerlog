# -*- coding: utf-8 -*-
import imgui

from src.model.mainconfig import MainConfig, ELogLevel


class MainView(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.last_sel_log = None
        self.config = MainConfig.main_config()
        self.log_level = ["Log", "Warning", "Error"]

        self.ID_CHILD_CONSOLE = "child_console"

    def update(self):
        imgui.set_next_window_size(self.width, self.height)
        imgui.set_next_window_position(0, 0)

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.begin("main view", False,
                    imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (6, 6))
        cur_style = imgui.get_style()
        padding = cur_style.window_padding
        cur_cursor_pos = imgui.get_cursor_pos()
        imgui.set_cursor_pos((cur_cursor_pos[0] + padding[0], cur_cursor_pos[1] + padding[1]))
        imgui.begin_child(self.ID_CHILD_CONSOLE, self.width - cur_style.window_padding[0] * 2, self.height - 120, True)

        for text in xrange(100):
            ret = imgui.selectable("log-----------------------------%s" % text, (self.last_sel_log==text), height=30)
            if ret[1]:
                self.last_sel_log = text
        # imgui.text("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

        imgui.end_child()
        imgui.pop_style_var()

        # 按纽栏
        cur_cursor_pos = imgui.get_cursor_pos()
        imgui.set_cursor_pos((cur_cursor_pos[0] + padding[0], cur_cursor_pos[1]))
        if imgui.button("clear"):
            print ("clear")
        imgui.same_line()

        # log level
        for log_level in xrange(ELogLevel.LOG, 3 + 1):
            is_check = self.config.is_has_log_level(log_level)
            ret = imgui.checkbox(self.log_level[log_level - 1], is_check)
            imgui.same_line()
            if ret[1] == is_check:
                continue
            if ret[1]:
                self.config.add_log_level(log_level)
            else:
                self.config.remove_log_level(log_level)


        imgui.end()
        imgui.pop_style_var(2)
