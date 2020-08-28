# -*- coding: utf-8 -*-
import logging

import glfw, imgui

from src.common import utils
from src.model.mainconfig import MainConfig, EConfigKey
from src.view.buildin_style import TextColor


class MainView(object):

    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.config = MainConfig.main_config()
        self.log_level = ["Log", "Warning", "Error"]
        self.ID_CHILD_CONSOLE = "child_console"
        self.log_level_lst = [logging.INFO, logging.WARNING, logging.ERROR]
        self.sel_idx = None
        self.detail_idx = None
        self.is_open_detail = False
        self.is_edit_cmd = True
        self.cur_edit_txt = ""

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
        imgui.begin_child(self.ID_CHILD_CONSOLE, self.width - cur_style.window_padding[0] * 2, self.height - 80, True)

        search_text = self.config.get_string(EConfigKey.CONTENT_SEARCH_TEXT)
        win_width = imgui.get_window_width()
        for idx, record in enumerate(self.log_mgr.log_lst):
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
            imgui.push_id(str(idx))
            ret = imgui.selectable_wrap(record.msg_with_level,  idx == self.sel_idx, imgui.SELECTABLE_ALLOW_DOUBLE_CLICK,
                                        win_width*0.98, 30)
            if ret[1]:
                self.sel_idx = idx
            if imgui.is_item_hovered() and imgui.is_mouse_double_clicked(0):
                self.detail_idx = idx
                imgui.open_popup("detail_log_%d" % self.detail_idx)
            self.draw_log_detail_info_panel(idx, record)
            if old_color:
                utils.set_style_color(imgui.COLOR_TEXT, old_color)
            imgui.pop_id()

        if imgui.is_mouse_dragging() or imgui.get_io().mouse_wheel:
            if imgui.get_scroll_y() >= imgui.get_scroll_max_y():
                self.config.set_bool(EConfigKey.CONTENT_SCROLL_TO_BOTTOM, True)
            else:
                self.config.set_bool(EConfigKey.CONTENT_SCROLL_TO_BOTTOM, False)

        is_to_bottom = self.config.get_bool(EConfigKey.CONTENT_SCROLL_TO_BOTTOM, True)
        if is_to_bottom:
            imgui.set_scroll_y(imgui.get_scroll_max_y())

        imgui.end_child()
        imgui.pop_style_var()

    # 绘制某条log的详细信息
    def draw_log_detail_info_panel(self, idx, log):
        if idx != self.detail_idx:
            return
        popup_id = "detail_log_%s" % self.detail_idx

        win_size = imgui.get_window_size()
        item_size = (win_size.x * 0.94, win_size.y * 0.5)
        imgui.set_next_window_size(item_size[0], item_size[1])
        imgui.set_next_window_position((win_size.x - item_size[0]) * 0.5, (win_size.y - item_size[1]) * 0.5)
        if imgui.begin_popup(popup_id):
            msg = log.detail_info
            utils.get_win_size()
            btn_height = 22
            padding = imgui.get_style().window_padding
            area_size = (item_size[0] * 0.98, item_size[1] * 0.94 - btn_height - padding.y * 0.6)
            imgui.input_text_multiline("##hidden", msg, len(msg) + 1, area_size[0], area_size[1], imgui.INPUT_TEXT_READ_ONLY)
            if imgui.button("复制", area_size[0], btn_height):
                print ("复制")
            imgui.end_popup()

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
        old_text = self.config.get_string(EConfigKey.CONTENT_SEARCH_TEXT)
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

        # 是否固定到底部
        imgui.same_line()
        is_to_bottom = self.config.get_bool(EConfigKey.CONTENT_SCROLL_TO_BOTTOM, True)
        ret = imgui.checkbox("bottom", is_to_bottom)
        if ret[1] != is_to_bottom:
            self.config.set_bool(EConfigKey.CONTENT_SCROLL_TO_BOTTOM, ret[1])

    def draw_input_bar(self):
        utils.set_cursor_offset(6, 0)
        cur_cmd = self.config.get_current_cmd()
        cur_txt = self.cur_edit_txt if self.is_edit_cmd else cur_cmd
        # win_width = imgui.get_window_width()
        # win_height = imgui.get_window_height()
        imgui.push_item_width(520)
        imgui.push_id(EConfigKey.CONTENT_CMD_TXT)
        ret = imgui.input_text("", cur_txt, 1024, imgui.INPUT_TEXT_ENTER_RETURNS_TRUE|
                               imgui.INPUT_TEXT_CALLBACK_COMPLETION | imgui.INPUT_TEXT_CALLBACK_HISTORY
                               ,self.input_bar_callback)
        self.is_edit_cmd = ret[1] != cur_cmd
        if self.is_edit_cmd:
            self.cur_edit_txt = ret[1]
        if ret[0]:
            self._send_cmd(ret[1])
            # print "hello world", ret[1]
        imgui.pop_id()
        imgui.same_line()
        utils.set_cursor_offset(-8, 0)
        if imgui.button("发送命令"):
            self._send_cmd(ret[1])

    def _send_cmd(self, cmd):
        self.excute_cmd(cmd)
        imgui.set_item_default_focus()
        imgui.set_keyboard_focus_here(-1)

    def excute_cmd(self, cmd):
        if not cmd:
            return
        cmd = cmd.strip()
        if not cmd:
            return
        self.config.push_cmd(cmd)
        print ("excute_cmd", cmd)
        self.app.log_server.send(cmd)

    def input_bar_callback(self, data):
        print data
        if data.event_flag == imgui.INPUT_TEXT_CALLBACK_HISTORY:
            if data.event_key == imgui.KEY_DOWN_ARROW:
                self.config.change_current_cmd_idx(1)
            elif data.event_key == imgui.KEY_UP_ARROW:
                pos = self.config.get_current_cmd_pos()
                if pos == -1:
                    self.config.set_cmd_pos_to_last()
                elif pos > 0:
                    self.config.change_current_cmd_idx(-1)
            prev_cmd = data.buf
            cmd = self.config.get_current_cmd()
            if prev_cmd == cmd:
                return
            if data.buf_text_len > 0:
                data.delete_chars(0, data.buf_text_len)
            data.insert_chars(0, cmd)
        elif data.event_flag == imgui.INPUT_TEXT_CALLBACK_COMPLETION:
            print "complete"

    def on_search_text_change(self, new_text):
        self.config.set_string(EConfigKey.CONTENT_SEARCH_TEXT, new_text)
        print("on_search_text_change>>", new_text)

    def refresh(self, new_record):
        pass

    def on_close(self):
        self.config.save()
