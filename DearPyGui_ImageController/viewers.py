from __future__ import annotations

import traceback
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from PIL.Image import Image

from DearPyGui_Addons.handler_deleter import HandlerDeleter
from DearPyGui_Addons.loading_indicator_radius import get_loading_indicator_radius
from . import tools

if TYPE_CHECKING:
    from _typeshed import SupportsRead
    from .controller import SubscriptionTag, ImageControllerType, ControllerType
    from .tools import TextureTag

import dearpygui.dearpygui as dpg

from .controller import default_controller


class ImageViewerCreator(ABC):
    image: Image | None = None

    __controller: ControllerType | None = None
    __image_info: ImageControllerType | None = None
    __subscription_tag: SubscriptionTag | None = None

    def set_controller(self, controller: ControllerType = None):
        """
        Set the image controller.
        The next image loading will be done through this controller.

        :param controller: Set `None` if you want to set the default controller
        """
        self.__controller = controller

    def get_controller(self) -> ControllerType:
        if self.__controller is None:
            return default_controller
        return self.__controller

    def load(self, image: str | bytes | Path | SupportsRead[bytes] | Image = None, show_loading=False):
        self.image = None
        if show_loading:
            self.hide()

        if self.__image_info:
            self.__image_info.unsubscribe(self.__subscription_tag)
        self.__image_info, self.__subscription_tag = None, None

        if image is None:
            return self.hide() if not show_loading else None

        controller = self.get_controller()
        _, self.__image_info = controller.add(image)
        self.__subscription_tag = self.__image_info.subscribe(self)  # noqa
        self.image = self.__image_info.image  # TODO: to property

        if self.__image_info.loaded:
            self.show(self.__image_info.texture_tag)

    def unload(self):
        self.load(None)

    def update_last_time_visible(self):
        if self.__image_info:
            self.__image_info.update_last_time_visible()

    @abstractmethod
    def show(self, texture_tag: TextureTag):
        ...

    @abstractmethod
    def hide(self):
        ...

    def __del__(self):
        if self.__image_info:
            self.__image_info.unsubscribe(self.__subscription_tag)
        self.image = None
        self.__controller = None
        self.__image_info = None
        self.__subscription_tag = None


class ImageViewer(ImageViewerCreator):
    width: int | None = None
    height: int | None = None
    _theme: int = None

    group: int = None
    _view_window: int = None

    dpg_image: int | None = None
    _visible_handler: int = None
    image_handler: int | str | None = None

    @classmethod
    def _get_theme(cls) -> int:
        if cls._theme is None:
            with dpg.theme() as cls._theme:
                with dpg.theme_component(dpg.mvAll, parent=cls._theme) as theme_component:
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
        return cls._theme

    def _get_visible_handler(self) -> int:
        if not self._visible_handler:
            with dpg.item_handler_registry() as self._visible_handler:
                dpg.add_item_visible_handler(callback=self.update_last_time_visible, parent=self._visible_handler)
        return self._visible_handler

    def get_size(self) -> tuple[int, int]:
        if self.width and self.height:
            return self.width, self.height
        if not self.image:
            if self.width:
                return self.width, self.unload_height
            if self.height:
                return self.unload_width, self.height
            return self.unload_width, self.unload_height
        if not self.width and not self.height:
            return self.image.width, self.image.height
        if self.width:
            height = int(self.image.height * (self.width / self.image.width))
            return self.width, height
        if self.height:
            width = int(self.image.width * (self.height / self.image.height))
            return width, self.height

    def set_size(self, *, width: int = None, height: int = None):
        """
        Set the size of the viewer when the image is loaded in the viewer
        (is also used when dimensions are set and do not equal None).
        If the dimensions are None the size of the picture will be used.
        If one of the dimensions is None, it will be proportionally
        changed in the ratio of the image size to the other dimension.
        If a viewer is created, the changes are applied instantly.

        :param width: Viewer width. Used when the image is loaded in the viewer or another dimension is also set
        :param height: Viewer height. Used when the image is loaded in the viewer or another dimension is also set
        """
        self.width = width
        self.height = height
        if not self.group:
            return
        width, height = self.get_size()
        try:
            dpg.configure_item(self._view_window,
                               width=width,
                               height=height)
            if self.dpg_image:
                dpg.configure_item(self.dpg_image,
                                   width=width,
                                   height=height)
        except Exception:
            traceback.print_exc()

    def set_width(self, width: int = None):
        """
        It uses the function `.set_size` and only sets the width, the width will not be changed

        :param width: Viewer width. Used when the image is loaded in the viewer or another dimension is also set
        """
        self.set_size(width=width, height=self.height)

    def set_height(self, height: int = None):
        """
        It uses the function `.set_size` and only sets the height, the width will not be changed

        :param height: Viewer height. Used when the image is loaded in the viewer or another dimension is also set
        """
        self.set_size(width=self.width, height=height)

    def __init__(self,
                 image: str | bytes | Path | SupportsRead[bytes] | Image = None,
                 controller: ControllerType = None,
                 unload_width: int = 100,
                 unload_height: int = 100):
        """
        Image viewer, which automatically unloads the image
        from the DPG if the user can't see it.
        You can specify some arguments at creation if you want

        :param image: Pillow Image or the path to the image, or any other object that Pillow can open
        :param controller: Set `None` if you want to use the default controller
        :param unload_width: Viewer width, when the image is not yet loaded (or unloaded) from the viewer
        :param unload_height: Viewer height, when the image is not yet loaded (or unloaded) from the viewer
        """

        self.texture_tag = tools.get_texture_plug()

        self.unload_width = unload_width
        self.unload_height = unload_height
        if controller:
            self.set_controller(controller)
        if image:
            self.load(image)

    def set_image_handler(self, handler: int | str = None):
        """
        Set the DPG handler on the image.
        It will work even if the image is not loaded into the viewer.
        Not working during image loading.

        :param handler: DPG item handler
        """
        self.image_handler = handler
        if self.dpg_image:
            try:
                dpg.bind_item_handler_registry(self.dpg_image, self.image_handler)
            except Exception:
                pass

    def create(self,
               width: int = None,
               height: int = None,
               unload_width: int = None,
               unload_height: int = None,
               parent: int | str = 0):
        """
        Creates a viewer in the DPG, if it has already been created,
        moves it to a new place (deletes the old).
        If you have pre-specified the dimensions, you don't have to set them here.

        :param width: Viewer width. Used when the image is loaded in the viewer or another dimension is also set
        :param height: Viewer height. Used when the image is loaded in the viewer or another dimension is also set
        :param unload_width: Viewer width, when the image is not yet loaded (or unloaded) from the viewer. Not used if the size is set (`width` and `height` is not None)
        :param unload_height: Viewer height, when the image is not yet loaded (or unloaded) from the viewer. Not used if the size is set (`width` and `height` is not None)
        :param parent: Parent to add this item to. (runtime adding)
        """
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if unload_height is not None:
            self.unload_height = unload_height
        if unload_width is not None:
            self.unload_width = unload_width

        if self.group:
            try:  # If it was deleted with DPG
                dpg.delete_item(self.group)
            except Exception:
                pass
        width, height = self.get_size()
        with dpg.group(parent=parent) as self.group:
            dpg.bind_item_theme(self.group, self._get_theme())
            self._view_window = dpg.add_child_window(width=width,
                                                     height=height,
                                                     no_scrollbar=True,
                                                     parent=self.group)
            dpg.bind_item_handler_registry(self.group, self._get_visible_handler())

        if self.texture_tag == tools.get_texture_plug():
            self.hide()
        else:
            self.show(self.texture_tag)

    def show(self, texture_tag: TextureTag):
        self.texture_tag = texture_tag
        if not self.group:  # If not created
            return
        width, height = self.get_size()
        dpg.delete_item(self._view_window, children_only=True)
        dpg.configure_item(self._view_window, width=width, height=height)

        self.dpg_image = dpg.add_image(self.texture_tag,
                                       width=width,
                                       height=height,
                                       parent=self._view_window)
        if self.image_handler:
            dpg.bind_item_handler_registry(self.dpg_image, self.image_handler)

    def hide(self):
        self.texture_tag = tools.get_texture_plug()
        if self.group is None:  # If not created
            return
        self.dpg_image = None

        try:
            dpg.delete_item(self._view_window, children_only=True)
        except Exception:
            return

        width, height = self.get_size()
        if self.image:
            dpg.add_loading_indicator(parent=self._view_window, radius=get_loading_indicator_radius(width, height))
        else:
            dpg.configure_item(self._view_window, width=width, height=height)
            self.dpg_image = dpg.add_image(tools.get_texture_plug(),
                                           width=width,
                                           height=height,
                                           parent=self._view_window)

            if self.image_handler:
                dpg.bind_item_handler_registry(self.dpg_image, self.image_handler)

    def delete(self):
        """
        Deletes everything that was created by this object,
        namely: the viewer (DPG elements), handlers.
        Also resets all variables (except `unload_width` and `unload_height`)
        """
        self.__del__()

    def __del__(self):
        if self.group:
            try:  # If it was deleted with DPG
                dpg.delete_item(self.group)
            except Exception:
                pass
        self.width = None
        self.height = None

        self.group = None  # noqa
        self._view_window = None  # noqa
        self.texture_tag = tools.get_texture_plug()  # noqa

        super().__del__()

        if self._visible_handler:
            HandlerDeleter.add(self._get_visible_handler())
            self._visible_handler = None  # noqa
        self.image_handler = None
        self.controller = None
