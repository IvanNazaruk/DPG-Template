from pathlib import Path
from typing import Callable

import dearpygui.dearpygui as dpg

import DearPyGui_ImageController as dpg_img
import DearPyGui_Theme as dpg_theme
from DearPyGui_Addons import get_alpha_theme
from . import HandlerDeleter


class ImageCheckBox:
    value: bool = True

    _alpha_theme = None

    def _frame_padding_changed(self, value: list[float, float]):
        width, height = self.size
        width += value[0] * 2
        height += value[1] * 2
        self.image_viewer.set_size(width=width, height=height)

    def __init__(self, enable_image: Path, disable_image: Path,  # FIXME Use Textures
                 width: int = None, height: int = None, enabled: bool = True,
                 default_value: bool = True, callback: Callable = None, parent=0,
                 use_frame_padding: bool = False):
        self.enable_image = enable_image
        self.disable_image = disable_image
        self.enabled = enabled
        self.value = default_value
        self.callback = callback

        with dpg.item_handler_registry() as self.handler:
            dpg.add_item_clicked_handler(callback=self.on_click)

        self.group = dpg.add_group(parent=parent)
        self.image_viewer = dpg_img.ImageViewer()
        self.image_viewer.load(enable_image if default_value else disable_image)
        self.image_viewer.create(width=width, height=height, parent=self.group)
        self.image_viewer.set_image_handler(self.handler)

        self.size = self.image_viewer.get_size()

        if use_frame_padding:
            dpg_theme.subscribe_style_theme_change(dpg.mvStyleVar_FramePadding, self._frame_padding_changed)

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def on_click(self):
        if not self.enabled:
            return
        self.value = not self.value
        if self.value:
            self.image_viewer.load(self.enable_image)
            dpg.bind_item_theme(self.group, None)  # noqa
        else:
            self.image_viewer.load(self.disable_image)
            dpg.bind_item_theme(self.group, get_alpha_theme(0.6))
        if self.callback:
            self.callback()

    def __del__(self):
        self.delete()

    def delete(self):
        self.image_viewer.delete()
        HandlerDeleter.add(self.handler)
