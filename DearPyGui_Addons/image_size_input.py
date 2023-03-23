from typing import Callable

import dearpygui.dearpygui as dpg

import fonts
import textures
from .alpha_theme import get_alpha_theme
from .image_check_box import ImageCheckBox
from .dpg_input import IntInput


class ImageSizeInput:
    def __init__(self, width: int, height: int, callback: Callable = None, parent=0,
                 use_frame_padding: bool = False):
        self.default_width = width
        self.default_height = height
        self.callback = callback
        with dpg.group(parent=parent, horizontal=True) as self.group:
            self.width_input = IntInput(width, callback=self.width_updated, parent=self.group,
                                        use_frame_padding=use_frame_padding)
            self.use_proportions_checkbox = ImageCheckBox(textures.ChaineEnabled.get(), textures.ChaineDisabled.get(),
                                                          height=fonts.font_size, callback=self.checkbox_updated, parent=self.group,
                                                          use_frame_padding=use_frame_padding)
            self.height_input = IntInput(height, callback=self.height_updated, parent=self.group,
                                         use_frame_padding=use_frame_padding)

    def set_enabled(self, enabled: bool):
        if enabled:
            dpg.bind_item_theme(self.group, 0)
            if not self.use_proportions_checkbox.value:
                dpg.bind_item_theme(self.use_proportions_checkbox.group, get_alpha_theme(0.6))
        else:
            dpg.bind_item_theme(self.group, get_alpha_theme(0.25))
            dpg.bind_item_theme(self.use_proportions_checkbox.group, 0)

        self.width_input.set_enabled(enabled)
        self.use_proportions_checkbox.set_enabled(enabled)
        self.height_input.set_enabled(enabled)

    def get_value(self) -> list[int, int]:
        return [self.width_input.get_value(), self.height_input.get_value()]

    def set_value(self, size: list[int, int]):
        self.default_width, self.default_height = size
        self.width_input.set_value(self.default_width)
        self.height_input.set_value(self.default_height)

    def width_updated(self):
        if self.use_proportions_checkbox.value:
            width, height = self.width_input.get_value(), self.height_input.get_value()
            ratio = width / self.default_width
            height = int(ratio * self.default_height)
            self.height_input.set_value(height)
        if self.callback is not None:
            self.callback()

    def height_updated(self):
        if self.use_proportions_checkbox.value:
            width, height = self.width_input.get_value(), self.height_input.get_value()
            ratio = height / self.default_height
            width = int(ratio * self.default_width)
            self.width_input.set_value(width)
        if self.callback is not None:
            self.callback()

    def checkbox_updated(self):
        if not self.use_proportions_checkbox.value:
            return
        self.default_width, self.default_height = self.width_input.get_value(), self.height_input.get_value()

    def __del__(self):
        self.delete()

    def delete(self):
        self.width_input.delete()
        self.use_proportions_checkbox.delete()
        self.height_input.delete()
