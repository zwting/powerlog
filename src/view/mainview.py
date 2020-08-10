# -*- coding: utf-8 -*-
import logging

import imgui, glfw

from src.common import utils
from src.model.mainconfig import MainConfig, EConfigKey
from src.view.buildin_style import TextColor


class MainView(object):

    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.last_sel_log = None
        self.config = MainConfig.main_config()
        self.log_level = ["Log", "Warning", "Error"]
        self.ID_CHILD_CONSOLE = "child_console"
        self.log_level_lst = [logging.INFO, logging.WARNING, logging.ERROR]

        self.init()

    @property
    def log_mgr(self):
        from src.controller.log_mgr import LogMgr
        return LogMgr.instance()

    def init(self):
        pass

    def update(self):
        imgui.set_next_window_size(self.width, self.height)
        imgui.set_next_window_position(0, 0)

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.begin("main view", False,
                    imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE |
                    imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_TITLE_BAR)

        self.draw_menu()
        self.draw_logs()
        self.draw_btn_bar()
        self.draw_input_bar()
        
        imgui.end()
        imgui.pop_style_var(2)

    def draw_menu(self):
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (8, 8))
        if imgui.begin_menu_bar():
            # first menu dropdown
            if imgui.begin_menu('菜单', True):
                if utils.is_menu_item_click('导出', 'Ctrl+O+P', False, True):
                    print "暂不支持"
                if utils.is_menu_item_click('设置', 'Ctrl+Alt+S', False, True):
                    print "设置"
                imgui.end_menu()

            if imgui.begin_menu("工具", True):
                if utils.is_menu_item_click("查找", "Ctrl+F", False, True):
                    print "查找"
                if utils.is_menu_item_click("自定义GM", "Ctrl+G", False, True):
                    print "自定义GM"
                imgui.end_menu()

            if imgui.begin_menu("帮助", True):
                if utils.is_menu_item_click("文档", "F1", False, True):
                    print "文档"
                if utils.is_menu_item_click("快捷键", "Ctrl+M", False, True):
                    print "快捷键"
                if utils.is_menu_item_click("关于...", None, False, True):
                    print "关于"
                imgui.end_menu()

            imgui.end_menu_bar()
        imgui.pop_style_var()

    def draw_logs(self):
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (6, 6))
        cur_style = imgui.get_style()
        padding = cur_style.window_padding
        cur_cursor_pos = imgui.get_cursor_pos()
        imgui.set_cursor_pos((cur_cursor_pos[0] + padding[0], cur_cursor_pos[1] + padding[1]))
        imgui.begin_child(self.ID_CHILD_CONSOLE, self.width - cur_style.window_padding[0] * 2, self.height - 150, True)

        search_text = self.config.getString(EConfigKey.CONTENT_SEARCH_TEXT)
        for record in self.log_mgr.log_lst:
            if not self.config.is_has_log_level(record.level):
                continue
            if not utils.filter_search_text(search_text, record):
                continue
            old_color = None
            if record.level == logging.ERROR:
                old_color = utils.set_style_color(imgui.COLOR_TEXT, TextColor.ERed)
            elif record.level == logging.WARN or record.level == logging.WARNING:
                old_color = utils.set_style_color(imgui.COLOR_TEXT, TextColor.EYellow)
            elif record.level == logging.INFO:
                old_color = utils.set_style_color(imgui.COLOR_TEXT, TextColor.EWhite)
            imgui.push_id(record.create_time_in_str)
            imgui.push_text_wrap_pos(200)
            ret = imgui.selectable(record.msg_with_level, record == self.last_sel_log, height=30)
            if ret[1]:
                self.last_sel_log = record
            if old_color:
                utils.set_style_color(imgui.COLOR_TEXT, old_color)
            imgui.pop_id()

        imgui.end_child()
        imgui.pop_style_var()

    def draw_btn_bar(self):
         # 按钮栏
        utils.set_cursor_offset(6, 0)
        if imgui.button("clear"):
            print ("清理")
            self.log_mgr.clear()
        imgui.same_line()

        # log等级
        for idx, log_level in enumerate(self.log_level_lst):
            is_check = self.config.is_has_log_level(log_level)
            ret = imgui.checkbox(self.log_level[idx], is_check)
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
        imgui.push_item_width(win_width - 20)
        imgui.push_id(EConfigKey.CONTENT_CMD_TXT)
        ret = imgui.input_text("", cur_cmd, 2056, imgui.INPUT_TEXT_ENTER_RETURNS_TRUE |
                               imgui.INPUT_TEXT_CALLBACK_COMPLETION | imgui.INPUT_TEXT_CALLBACK_HISTORY
                               , None)
        if ret[0]:
            self.app.log_server.send(ret[1])
            imgui.set_keyboard_focus_here(1)
            # print "hello world", ret[1]
        imgui.pop_id()

    def on_search_text_change(self, new_text):
        self.config.setString(EConfigKey.CONTENT_SEARCH_TEXT, new_text)
        print("on_search_text_change>>", new_text)

    def refresh(self, new_record):

        pass