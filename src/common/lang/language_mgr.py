# -*- coding: utf-8 -*-

class ELanguageType(object):
    Chinese = 1
    English = 2

class LangMgr(object):
    _instance = None

    @staticmethod
    def instance():
        if not LangMgr._instance:
            LangMgr._instance = LangMgr()
        return LangMgr._instance

    def __init__(self, init_lang=ELanguageType.Chinese):
        self.lang = init_lang
        self.dict = {}

    def _load_lang_data(self):
        pass

    def get_text(self, key):
        if self.lang not in self.dict:
            self.dict[self.lang] = {}
        if key not in self.dict[self.lang]:
            return key
        return self.dict[self.lang][key]
