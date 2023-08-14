import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Demo WIP", width=600, height=300, x_pos=1920 // 2 - 300, y_pos=1080 // 2 - 400)


def main():
    from gui import MainWindow
    main_window = MainWindow()
    dpg.set_primary_window(main_window.window, True)


import sys

if sys.platform.startswith('win'):
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation')
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

dpg.configure_viewport(0, clear_color=(255, 255, 255))
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.render_dearpygui_frame()

import DearPyGui_DragAndDrop as dpg_dnd

import DPG_modules.Animations as dpg_anim
import DPG_modules.Theme as dpg_theme
from DPG_modules.Addons.title_bar import set_dark_mode
from Resources import fonts, settings

dpg_dnd.initialize()
settings.load_settings()
dpg.bind_font(fonts.load(show=False))
dpg.bind_theme(dpg_theme.initialize())

set_dark_mode(True)

dpg.set_frame_callback(dpg.get_frame_count() + 1, main)
while dpg.is_dearpygui_running():
    dpg_anim.update()
    dpg.render_dearpygui_frame()
dpg.destroy_context()
