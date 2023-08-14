from functools import cache

import dearpygui.dearpygui as dpg


@cache
def get_button_is_text_theme():
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvButton, parent=theme) as theme_component:
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0), parent=theme_component)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0), parent=theme_component)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 0), parent=theme_component)
    return theme
