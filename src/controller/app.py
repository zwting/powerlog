# -*- coding: utf-8 -*-

import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

from src.controller.log_server import LogServer, PowerLogHandler
from src.view.mainview import MainView

g_size = 1280, 720

class App(object):
    _instance = None

    @staticmethod
    def instance():
        return App._instance

    @staticmethod
    def create_app(width, height):
        if App._instance:
            return App._instance
        App._instance = App(width, height)
        return App._instance

    def __init__(self, width, height):
        global g_size
        self.width = width
        self.height = height
        g_size = width, height
        self.window = None
        self.main_view = MainView(self, width, height)
        self.log_server = LogServer(PowerLogHandler())
        # log_server_old.main()
        self.start()

    def update(self):
        if not self.main_view:
            return
        self.log_server.receive()
        self.main_view.update()

    def start(self):
        imgui.create_context()
        io = imgui.get_io()
        # io.fonts.add_font_default()
        io.fonts.add_font_from_file_ttf("./res/font/Roboto-Medium.ttf", 14, io.fonts.get_glyph_ranges_chinese_full())
        io.fonts.add_font_from_file_ttf("./res/font/FZY3JW.ttf", 13, io.fonts.get_glyph_ranges_chinese_full(), True)
        self.window = App._impl_glfw_init()
        impl = GlfwRenderer(self.window)

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            impl.process_inputs()
            imgui.new_frame()
            # imgui.show_test_window()

            self.update()

            gl.glClearColor(1., 1., 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.main_view and self.main_view.on_close()
        impl.shutdown()
        glfw.terminate()


    @staticmethod
    def _impl_glfw_init():
        global g_size
        width, height = g_size
        window_name = "minimal ImGui/GLFW3 example"

        if not glfw.init():
            print("Could not initialize OpenGL context")
            exit(1)

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)

        # Create a windowed mode window and its OpenGL context
        window = glfw.create_window(
            int(width), int(height), window_name, None, None
        )
        glfw.make_context_current(window)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            exit(1)

        return window