from typing import Callable

import dearpygui.dearpygui as dpg

import DearPyGui_Theme as dpg_theme
from .handler_deleter import HandlerDeleter
from .dpg_get_text_size import get_text_size


class IntInput:
    dpg_object: int
    handler: int

    release_callback_tag = None
    now_value: int

    def _frame_padding_changed(self, value: list[float, float]):
        width = get_text_size(str(self.get_value()))[0]
        width += value[0] * 2
        dpg.set_item_width(self.dpg_object, int(width))

    def _verify_value(self, value: int) -> int:
        max_value = dpg.get_item_configuration(self.dpg_object)['max_value']
        if value > max_value:
            return max_value
        min_value = dpg.get_item_configuration(self.dpg_object)['min_value']
        if value < min_value:
            return min_value
        return value

    def set_enabled(self, enabled: bool):
        dpg.configure_item(self.dpg_object, enabled=enabled)

    def get_value(self):
        return self._verify_value(dpg.get_value(self.dpg_object))

    def set_value(self, value: int):
        dpg.set_value(self.dpg_object, self._verify_value(value))
        self.unselect()

    def __init__(self, default_value: int, min_value: int = 1, max_value: int = 1_000_000_000,
                 callback: Callable = None, parent=0, use_frame_padding: bool = False):
        self.use_frame_padding = use_frame_padding
        self.callback = callback
        self.dpg_object = dpg.add_input_int(default_value=int(default_value), min_value=min_value, max_value=max_value,
                                            step=0, step_fast=0, parent=parent)
        self.now_value = default_value
        with dpg.item_handler_registry() as self.handler:
            dpg.add_item_clicked_handler(callback=self.selected)
            dpg.add_item_deactivated_handler(callback=self.unselect)
        dpg.bind_item_handler_registry(self.dpg_object, self.handler)
        dpg.set_item_callback(self.dpg_object, self.selected)
        if use_frame_padding:
            dpg_theme.subscribe_style_theme_change(dpg.mvStyleVar_FramePadding, self._frame_padding_changed)
        self.unselect()

    def selected(self):
        if not dpg.get_item_configuration(self.dpg_object)['enabled']:
            return
        new_value = dpg.get_value(self.dpg_object)
        value = str(new_value) + '___'
        width = get_text_size(value)[0]
        if self.use_frame_padding:
            width += dpg_theme.get_current_theme_style_value(dpg.mvStyleVar_FramePadding)[0] * 2
        dpg.set_item_width(self.dpg_object, int(width))
        if self.now_value != new_value:
            self.now_value = new_value
            if self.callback:
                self.callback()

    def unselect(self):
        value = str(self.get_value())
        width = get_text_size(value)[0]
        if self.use_frame_padding:
            width += dpg_theme.get_current_theme_style_value(dpg.mvStyleVar_FramePadding)[0] * 2
        dpg.set_item_width(self.dpg_object, int(width))
        dpg.configure_item(self.dpg_object, default_value=int(value))

    def __del__(self):
        self.delete()

    def delete(self):
        HandlerDeleter.add(self.handler)
