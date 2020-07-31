# -*- coding: utf-8 -*-
import imgui

from src.common import utils


class TextColor(object):
    EError = utils.hex_2_vec4("cc423b")
    EWarning = utils.hex_2_vec4("cc9a06")
    ELog = utils.hex_2_vec4("c0c0c0")
    ERed = imgui.Vec4(1, 0, 0, 1)
    EGreen = imgui.Vec4(0, 1, 0, 1)
    EBlue = imgui.Vec4(0, 0, 1, 1)
    EYellow = imgui.Vec4(1, 1, 0, 1)
    EWhite = imgui.Vec4(1,1,1,1)