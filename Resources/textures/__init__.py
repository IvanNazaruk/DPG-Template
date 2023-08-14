import itertools
import traceback
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Sequence

import dearpygui.dearpygui as dpg
from PIL import Image

from DPG_modules import Theme as dpg_theme
from DPG_modules.Addons import dpg_callback, fix_color
from DPG_modules.ImageController import ImageController, ImageViewer
from DPG_modules.ImageController import get_texture_plug, image_to_dpg_texture

try:
    import numpy as np


    def change_color(image: Image.Image,
                     old_color: tuple[int, ...],
                     new_color: tuple[int, ...]) -> Image:
        old_color, new_color = old_color[:3], new_color[:3]

        data = np.array(image)  # "data" is a height x width x 4 numpy array # noqa
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        color_areas = (red == old_color[0]) & (blue == old_color[1]) & (green == old_color[2])
        data[..., :-1][color_areas.T] = new_color  # Transpose back needed # noqa
        return Image.fromarray(data)  # noqa
except ModuleNotFoundError:
    def change_color(image: Image.Image,
                     old_color: tuple[int],
                     new_color: tuple[int]) -> Image.Image:
        old_color, new_color = old_color[:3], new_color[:3]

        new_image = image.copy()
        data = new_image.load()
        width, height = image.size

        for x, y in itertools.product(range(width), range(height)):
            if data[x, y][:3] == old_color:
                data[x, y] = new_color + (data[x, y][3],)
        return new_image


class Texture(ABC):
    path: Path

    accent_color = (0, 0, 0)

    default_image: Image.Image
    image_viewer: ImageViewer
    image_controller: ImageController

    change_color_function: Callable[[Sequence[int]], None]

    @classmethod
    def init(cls):
        cls.image_viewer = ImageViewer(cls.path)  # noqa
        _, cls.image_controller = cls.image_viewer.get_controller().add(cls.path)  # noqa
        controller_image = cls.image_controller.image
        if controller_image.mode != "RGBA":
            cls.default_image = controller_image.convert("RGBA")
            if hasattr(controller_image, 'filename'):
                cls.default_image.filename = controller_image.filename
        cls.__post_init__()

    @classmethod
    def __post_init__(cls):
        ...

    @classmethod
    def get(cls):
        if not hasattr(cls, 'image_controller'):
            cls.init()
        return cls.path

    @classmethod
    def __change_color__(cls, new_color: Sequence[int]):
        if not hasattr(cls, 'image_controller'):
            cls.init()
        new_color = tuple(fix_color(new_color)[:3:])
        new_image = change_color(cls.default_image, cls.accent_color, new_color)
        cls.image_controller.image = new_image
        if cls.image_controller.loaded:
            cls.image_controller.loading = True
            old_texture_tag = cls.image_controller.texture_tag
            cls.image_controller.load(
                image_to_dpg_texture(cls.image_controller.image)
            )
            if old_texture_tag != get_texture_plug():
                try:
                    dpg.delete_item(old_texture_tag)
                except Exception:
                    traceback.print_exc()
        dpg.split_frame()

    @classmethod
    @abstractmethod
    def change_color(cls, new_color: Sequence[int]):
        cls.__change_color__(new_color)


class TextThemeTexture(Texture, ABC):
    path: Path

    @classmethod
    def __post_init__(cls):
        from DPG_modules.Theme import CurrentTheme

        dpg_theme.subscribe_color_theme_change(
            dpg.mvThemeCol_Text,
            lambda color: cls.change_color(color) if CurrentTheme.changing_progress == 1 else None
        )

    @classmethod
    @dpg_callback(sender=True)
    def change_color(cls, new_color: Sequence[int]):
        cls.__change_color__(new_color)


class ChaineEnabled(TextThemeTexture):
    path: Path = "./Resources/textures/files/64x64/chain_enabled.png"


class ChaineDisabled(TextThemeTexture):
    path: Path = "./Resources/textures/files/64x64/chain_disabled.png"
