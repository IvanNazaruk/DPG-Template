from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import dearpygui.dearpygui as dpg
from PIL.Image import Image

from . import ControllerType
from . import ImageViewer

if TYPE_CHECKING:
    from _typeshed import SupportsRead
    from pathlib import Path


class TooltipImageViewer(ImageViewer):
    def __init__(self,
                 parent: int | str,
                 image: str | bytes | Path | SupportsRead[bytes] | Image = None,
                 controller: ControllerType = None, ):
        super().__init__(image=image, controller=controller)
        self.set_size(width=1, height=1)
        with dpg.tooltip(parent=parent) as self.tooltip:
            self.create(parent=self.tooltip)

    def update_last_time_visible(self):  # TODO: rewrite this (work wrong)
        viewport_size = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]
        mouse_pos = dpg.get_mouse_pos(local=False)
        mouse_pos[0] += 25
        viewport_size[0] -= mouse_pos[0]
        viewport_size[1] -= 25

        if viewport_size[0] <= 0:
            viewport_size[0] = 1
        if viewport_size[1] <= 0:
            viewport_size[1] = 1

        width, height = None, None
        if viewport_size[0] >= self.image.width and viewport_size[1] >= self.image.height:
            pass
        elif viewport_size[0] < self.image.width and viewport_size[1] > self.image.height:
            width = viewport_size[0]
        elif viewport_size[0] > self.image.width and viewport_size[1] < self.image.height:
            height = viewport_size[1]
        else:  # viewport_size[0] < self.image.width and viewport_size[1] < self.image.height
            width_factor = viewport_size[0] / self.image.width
            height_factor = viewport_size[1] / self.image.height

            scale_factor = min(width_factor, height_factor)
            width = int(self.image.width * scale_factor)
            height = int(self.image.height * scale_factor)
        self.set_size(width=width, height=height)
        super().update_last_time_visible()

    def __del__(self):
        super().__del__()
        with contextlib.suppress(Exception):
            dpg.delete_item(self.tooltip)


def resize_image_to_fit_screen_resolution(image: Image):
    from Resources.settings import MaxTooltipImageHeight, MaxTooltipImageWidth
    screen_width: int
    screen_height: int
    screen_width, screen_height = MaxTooltipImageWidth.get(), MaxTooltipImageHeight.get()

    img_width, img_height = image.size

    # new_size = (img_width, img_height)
    if img_width > screen_width or img_height > screen_height:
        width_scale = screen_width / img_width
        height_scale = screen_height / img_height

        scale = min(width_scale, height_scale)
        new_size = (int(img_width * scale), int(img_height * scale))
        image = image.resize(new_size)
    return image
