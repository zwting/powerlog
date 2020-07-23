# -*- coding: utf-8 -*-
import imgui

from src.common import utils
from src.model.mainconfig import MainConfig, ELogLevel, EConfigKey


class MainView(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.last_sel_log = None
        self.config = MainConfig.main_config()
        self.log_level = ["Log", "Warning", "Error"]

        self.ID_CHILD_CONSOLE = "child_console"

        self.init()

    def init(self):
        pass

    def update(self):
        imgui.set_next_window_size(self.width, self.height)
        imgui.set_next_window_position(0, 0)

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.begin("main view", False,
                    imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

        self.draw_logs()

        self.draw_btn_bar()

        self.draw_input_bar()
        
        imgui.end()
        imgui.pop_style_var(2)

    def draw_logs(self):
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (6, 6))
        cur_style = imgui.get_style()
        padding = cur_style.window_padding
        cur_cursor_pos = imgui.get_cursor_pos()
        imgui.set_cursor_pos((cur_cursor_pos[0] + padding[0], cur_cursor_pos[1] + padding[1]))
        imgui.begin_child(self.ID_CHILD_CONSOLE, self.width - cur_style.window_padding[0] * 2, self.height - 120, True)

        for text in xrange(100):
            ret = imgui.selectable("log---我是--------------------------%s" % text, (self.last_sel_log==text), height=30)
            if ret[1]:
                self.last_sel_log = text
        # imgui.text("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

        imgui.end_child()
        imgui.pop_style_var()

    def draw_btn_bar(self):
         # 按钮栏
        utils.set_cursor_offset(6, 0)
        if imgui.button("clear"):
            print ("清理")
        imgui.same_line()

        # log等级
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

        # 搜索框
        imgui.same_line()
        old_text = self.config.getString(EConfigKey.CONTENT_SEARCH_TEXT)
        imgui.push_item_width(240)
        imgui.push_id(EConfigKey.CONTENT_SEARCH_TEXT)
        ret = imgui.input_text("", old_text, 128)
        imgui.pop_id()
        if ret[0]:
            self.on_search_text_change(ret[1])
        imgui.pop_item_width()
        imgui.same_line()
        utils.set_cursor_offset(-8, 0)
        if imgui.button("清空"):
            self.on_search_text_change("")

    def draw_input_bar(self):
        cur_cmd = self.config.get_current_cmd()
        win_width = imgui.get_window_width()
        imgui.push_id(EConfigKey.CONTENT_CMD_TXT)
        ret = imgui.input_text_multiline("", cur_cmd, 2056, win_width - 20, 60)
        
        imgui.pop_id()

    def on_search_text_change(self, new_text):
        self.config.setString(EConfigKey.CONTENT_SEARCH_TEXT, new_text)
        print("on_search_text_change>>", new_text)
