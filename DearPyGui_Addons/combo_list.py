from typing import Callable

import dearpygui.dearpygui as dpg

import DearPyGui_Theme as dpg_theme
from .dpg_get_text_size import get_text_size


class ComboList:
    dpg_object: int
    handler: int

    release_callback_tag = None
    now_value: str = ''

    def get_value(self):
        return dpg.get_value(self.dpg_object)

    def _frame_padding_changed(self, value: list[float, float]):
        width = get_text_size(self.get_value())[0]
        width += value[1] * 2
        dpg.set_item_width(self.dpg_object, int(width))

    def __init__(self, items: list[str], default_value: str = None, no_arrow_button: bool = True,
                 callback: Callable = None, parent=0, use_frame_padding: bool = False):
        self.use_frame_padding = use_frame_padding
        self.callback = callback
        if default_value is None:
            if len(items) == 0:
                default_value = '-'
            else:
                default_value = items[0]
        self.dpg_object = dpg.add_combo(items, default_value=default_value, no_arrow_button=no_arrow_button, parent=parent)
        self.now_value = default_value
        with dpg.item_handler_registry() as self.handler:
            dpg.add_item_clicked_handler(callback=self.selected)
            dpg.add_item_deactivated_handler(callback=self.unselect)
        dpg.bind_item_handler_registry(self.dpg_object, self.handler)
        dpg.set_item_callback(self.dpg_object, self.selected)
        if self.use_frame_padding:
            dpg_theme.subscribe_style_theme_change(dpg.mvStyleVar_FramePadding, self._frame_padding_changed)
        self.unselect()

    def set_enabled(self, enabled: bool):
        dpg.configure_item(self.dpg_object, enabled=enabled)

    def set_value(self, value: str):
        width = get_text_size(value)[0]
        if self.use_frame_padding:
            width += dpg_theme.get_current_theme_style_value(dpg.mvStyleVar_FramePadding)[0] * 2
        dpg.set_item_width(self.dpg_object, int(width))
        dpg.set_value(self.dpg_object, value)

    def selected(self):
        if not dpg.get_item_configuration(self.dpg_object)['enabled']:
            return
        value = new_value = str(self.get_value())
        if len(value) == 0:
            value = '-'
        width = get_text_size(value)[0]
        if self.use_frame_padding:
            width += dpg_theme.get_current_theme_style_value(dpg.mvStyleVar_FramePadding)[0] * 2
        dpg.set_item_width(self.dpg_object, int(width))
        if self.now_value != new_value:
            self.now_value = new_value
            if self.callback is not None:
                self.callback()

    def unselect(self):
        value = str(self.get_value())
        if len(value) == 0:
            value = '-'
        width = get_text_size(value)[0]
        if self.use_frame_padding:
            width += dpg_theme.get_current_theme_style_value(dpg.mvStyleVar_FramePadding)[0] * 2
        dpg.set_item_width(self.dpg_object, int(width))
