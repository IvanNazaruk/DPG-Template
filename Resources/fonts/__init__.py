from __future__ import annotations

import ctypes
import sys

import dearpygui.dearpygui as dpg

from DPG_modules import ImageController as dpg_img

font_size = 25
default_path = './Resources/fonts/InterTight-Regular.ttf'
font_registry = None
global_font = 0
print(sys.executable)


def add_font(file, size: int | float, parent=0, **kwargs) -> int:
    if not isinstance(size, (int, float)):
        raise ValueError(f'font size must be an integer or float. Not {type(size)}')

    chars = ['▶', '×', '✖', '—', '■', '○', '↗']
    for i, char in enumerate(chars):
        chars[i] = ord(char)

    with dpg.font(file, size, parent=parent, **kwargs) as font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent=font)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent=font)
        dpg.add_font_chars(chars, parent=font)
    return font


def load(show=False) -> int:
    """
    :return: default font
    """
    global font_registry, global_font
    dpg_img.set_texture_registry(dpg.add_texture_registry(show=show))
    dpg_img.default_controller.max_inactive_time = 3.5
    dpg_img.default_controller.unloading_check_sleep_time = 1.75

    font_registry = dpg.add_font_registry()
    global_font = add_font(default_path, font_size, parent=font_registry)
    return global_font
