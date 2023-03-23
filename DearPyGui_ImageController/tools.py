from __future__ import annotations

from typing import TypeVar

import dearpygui.dearpygui as dpg
from PIL.Image import Image

TextureTag = TypeVar('TextureTag', bound=int)

try:
    import numpy as np


    def _image_to_1d_array(image: Image) -> np.array:
        return np.array(image, dtype=np.float32).ravel() / 255  # noqa
except ModuleNotFoundError:
    import logging

    logger = logging.getLogger('DearPyGui_ImageController')
    logger.warning("numpy not installed. In DPG images will take longer to load (about 8 times slower).")


    def _image_to_1d_array(image: Image) -> list:
        img_1D_array = []
        image_data = image.getdata()
        if len(image_data) == 3:
            for pixel in image_data:
                img_1D_array.extend((pixel[0] / 255, pixel[1] / 255, pixel[2] / 255, 1))
        else:
            for pixel in image_data:
                img_1D_array.extend((pixel[0] / 255, pixel[1] / 255, pixel[2] / 255, pixel[3] / 255))
        del image_data
        return img_1D_array

texture_registry: int | str = 0
texture_plug: TextureTag = None  # noqa


def set_texture_registry(texture_registry_tag: int | str):
    global texture_registry
    texture_registry = texture_registry_tag


def get_texture_registry() -> int | str:
    return texture_registry


def get_texture_plug() -> TextureTag:
    global texture_plug
    if texture_plug is None:
        texture_plug = dpg.add_static_texture(width=1,
                                              height=1,
                                              default_value=[0] * 4,
                                              parent=texture_registry)
    return texture_plug


def image_to_dpg_texture(image: Image) -> TextureTag:
    rgba_image = image.convert("RGBA")
    img_1d_array = _image_to_1d_array(rgba_image)
    dpg_texture_tag = dpg.add_static_texture(width=rgba_image.width,
                                             height=rgba_image.height,
                                             default_value=img_1d_array,
                                             parent=texture_registry)

    rgba_image.close()
    del img_1d_array, rgba_image
    return dpg_texture_tag


def resize_image_to_fit_screen_resolution(image: Image):
    from settings import MaxTooltipImageHeight, MaxTooltipImageWidth
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
