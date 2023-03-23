import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd

import DearPyGui_Animations as dpg_anim
import DearPyGui_Theme as dpg_theme
import fonts
import settings

dpg.create_context()
dpg_dnd.initialize()
dpg.bind_theme(dpg_theme.initialize())
dpg.bind_font(fonts.load(show=False))
settings.load_settings()


def main():
    import gui
    main_widow = gui.MainWindow()
    dpg.set_primary_window(main_widow.window, True)


dpg.set_frame_callback(1, main)
dpg.setup_dearpygui()
dpg.create_viewport(title="Demo WIP", width=fonts.font_size * 30, height=fonts.font_size * 25,
                    clear_color=dpg_theme.get_current_theme_color_value(dpg.mvThemeCol_WindowBg))
dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg_anim.update()
    dpg.render_dearpygui_frame()
dpg.destroy_context()
