# -*- coding: utf-8 -*-
from src.common import utils
import os

config_file_path = os.path.join(os.getcwd(), "config", "config.json")

class EConfigKey(object):
    LOG_LEVEL_LIST = "LOG_LEVEL_LIST"           # log等级勾选状态
    CONTENT_SEARCH_TEXT = "CONTENT_SEARCH_TEXT" # 搜索框内容
    CONTENT_CMD_TXT = "CONTENT_CMD_TXT"         # 命令框历史记录
    CONTENT_CMD_IDX = "CONTENT_CMD_IDX"         # 命令框历史记录指针
    CONTENT_CMD_MAX_COUNT = "CONTENT_CMD_MAX_COUNT" # 命令框历史记录最大值
    CONTENT_SCROLL_TO_BOTTOM = "CONTENT_SCROLL_TO_BOTTOM"   #log是否固定到底部


class MainConfig(object):
    _instance = None

    @staticmethod
    def main_config():
        if not MainConfig._instance:
            MainConfig._instance = MainConfig()
        return MainConfig._instance

    def __init__(self):
        self.config = {}
        self.load()

    # 历史记录最大值
    @property
    def max_cmd_history_count(self):
        return self.config.setdefault(EConfigKey.CONTENT_CMD_MAX_COUNT, 20)

    def add_log_level(self, log_level):
        log_level_list = self.config.setdefault(EConfigKey.LOG_LEVEL_LIST, [])
        if log_level in log_level_list:
            return
        log_level_list.append(log_level)

    def remove_log_level(self, log_level):
        self.config.setdefault(EConfigKey.LOG_LEVEL_LIST, []).remove(log_level)

    def is_has_log_level(self, log_level):
        return log_level in self.config.get(EConfigKey.LOG_LEVEL_LIST, [])

    def push_cmd(self, cmd_str):
        if not cmd_str or not isinstance(cmd_str, str):
            return
        lst = self.config.setdefault(EConfigKey.CONTENT_CMD_TXT, [])
        self.config[EConfigKey.CONTENT_CMD_IDX] = -1
        lst.append(cmd_str)
        if len(lst) > self.max_cmd_history_count:
            lst.pop(0)

    # 获取当前指针所指的命令
    def get_current_cmd(self):
        lst = self.config.get(EConfigKey.CONTENT_CMD_TXT, None)
        if not lst:
            return ""
        cur_idx = self.config.get(EConfigKey.CONTENT_CMD_IDX, -1)
        if cur_idx == -1:
            return ""
        if 0 <= cur_idx < len(lst):
            return lst[cur_idx]
        self.config[EConfigKey.CONTENT_CMD_IDX] = -1
        return ""

    # 获取当前历史指令指针的位置
    def get_current_cmd_pos(self):
        return self.config.get(EConfigKey.CONTENT_CMD_IDX, -1)

    # 设置命令指针到最后
    def set_cmd_pos_to_last(self):
        lst = self.config.setdefault(EConfigKey.CONTENT_CMD_TXT, [])
        if not lst:
            return
        self.config[EConfigKey.CONTENT_CMD_IDX] = len(lst) - 1

    def change_current_cmd_idx(self, step):
        idx = self.config.setdefault(EConfigKey.CONTENT_CMD_IDX, 0)
        self.config[EConfigKey.CONTENT_CMD_IDX] = \
            utils.clamp(0, min(self.max_cmd_history_count - 1, len(self.config.get(EConfigKey.CONTENT_CMD_TXT)) - 1), idx + step)

    def get_string(self, key):
        return self.config.get(key, "")

    def set_string(self, key, value=None):
        if not key:
            return
        self.config[key] = value

    def get_bool(self, key, default_val=False):
        return self.config.get(key, default_val)

    def set_bool(self, key, value=False):
        if not key:
            return
        self.config[key] = value

    def save(self):
        global config_file_path
        import json
        with open(config_file_path, "w") as f:
            json_str = json.dumps(self.config)
            f.write(json_str)
            f.flush()

    def load(self):
        global config_file_path
        import json
        if not os.path.exists(config_file_path):
            self.config = {}
            return
        with open(config_file_path, "r") as f:
            try:
                json_str = f.read()
                self.config = json.loads(json_str)
            except Exception as err:
                self.config = {}
                print err


