from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image

from .controller import Controller
from .controller import default_controller
from .controller import ENABLE_LOADING
from .controller import ImageController
from .tools import _image_to_1d_array as image_to_1d_array
from .tools import get_texture_plug, image_to_dpg_texture
from .tools import get_texture_registry, set_texture_registry
from .tooltip import TooltipImageViewer
from .viewers import ImageViewer

if TYPE_CHECKING:
    from _typeshed import SupportsRead


def add_image(image: bytes | Path | SupportsRead[bytes] | Image,
              width: int = None,
              height: int = None,
              parent: int | str = 0,
              controller: Controller = None) -> ImageViewer:
    image_viewer = ImageViewer()
    image_viewer.set_controller(controller)
    image_viewer.load(image)
    image_viewer.set_size(width=width, height=height)
    image_viewer.create(parent=parent)
    return image_viewer
