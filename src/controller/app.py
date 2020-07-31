# -*- coding: utf-8 -*-

import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

from src.controller import log_server
from src.view.mainview import MainView


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
        self.width = width
        self.height = height
        self.window = None
        self.main_view = MainView(width, height)
        log_server.main()
        self.start(self.main_view.update)

    def start(self, update):
        self.update = update
        imgui.create_context()
        io = imgui.get_io()
        io.fonts.add_font_from_file_ttf("./res/font/FZZYJW.ttf", 12, io.fonts.get_glyph_ranges_chinese_full())
        self.window = App._impl_glfw_init()
        impl = GlfwRenderer(self.window)

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            # if imgui.begin_main_menu_bar():
            #     if imgui.begin_menu("File", True):
            #
            #         clicked_quit, selected_quit = imgui.menu_item(
            #             "Quit", 'Cmd+Q', False, True
            #         )
            #
            #         if clicked_quit:
            #             exit(1)
            #
            #         imgui.end_menu()
            #     imgui.end_main_menu_bar()

            imgui.show_test_window()

            if self.update and callable(self.update):
                self.update()

            gl.glClearColor(1., 1., 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        impl.shutdown()
        glfw.terminate()


    @staticmethod
    def _impl_glfw_init():
        width, height = 1280, 720
        window_name = "minimal ImGui/GLFW3 example"

        if not glfw.init():
            print("Could not initialize OpenGL context")
            exit(1)

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

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