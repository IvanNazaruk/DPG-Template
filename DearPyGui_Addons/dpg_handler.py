import traceback
from abc import ABC, abstractmethod
from typing import Callable, TypeVar

import dearpygui.dearpygui as dpg

SubscriptionTag = TypeVar('SubscriptionTag', bound=int)


class HandlerRegistry:
    handler: int = None

    @classmethod
    def get(cls):
        if cls.handler is None:
            cls.handler = dpg.add_handler_registry()
        return cls.handler


class HandlerCreator(ABC):
    handler: int | str = None

    subscribers: dict[int, Callable] = None

    @classmethod
    @abstractmethod
    def create_handler(cls):
        ...

    @classmethod
    def add(cls, function: Callable) -> SubscriptionTag:
        if cls.handler is None:
            cls.handler = cls.create_handler()
        if cls.subscribers is None:
            cls.subscribers = {}
        subscription_tag = dpg.generate_uuid()
        cls.subscribers[subscription_tag] = function
        return subscription_tag

    @classmethod
    def remove(cls, subscription_tag: SubscriptionTag):
        if subscription_tag in cls.subscribers:
            del cls.subscribers[subscription_tag]

    @classmethod
    def callback(cls):
        for function in list(cls.subscribers.values()):
            try:
                function()
            except Exception:
                traceback.print_exc()


class MouseDownHandler(HandlerCreator):
    @classmethod
    def create_handler(cls) -> int:
        return dpg.add_mouse_down_handler(callback=cls.callback, parent=HandlerRegistry.get())


class MouseReleaseHandler(HandlerCreator):
    @classmethod
    def create_handler(cls) -> int:
        return dpg.add_mouse_release_handler(callback=cls.callback, parent=HandlerRegistry.get())


class ViewportResizeHandler(HandlerCreator):
    @classmethod
    def create_handler(cls) -> int:
        dpg.set_viewport_resize_callback(cls.callback)
        return dpg.generate_uuid()


add_mouse_down_callback = MouseDownHandler.add
add_mouse_release_callback = MouseReleaseHandler.add
add_viewport_resize_callback = ViewportResizeHandler.add

remove_mouse_down_callback = MouseDownHandler.remove
remove_mouse_release_callback = MouseReleaseHandler.remove
remove_viewport_resize_callback = ViewportResizeHandler.remove
