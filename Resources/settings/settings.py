import traceback
from abc import ABC
from typing import Any, Callable

import dearpygui.dearpygui as dpg


class SettingValue(ABC):
    value: Any
    subscribers: dict[int, Callable[[], None]] = None

    @classmethod
    def set(cls, value) -> None:
        need_callback = value != cls.value
        cls.value = value
        if need_callback:
            # print(cls.__name__, cls.get(), "->", value)
            cls.callback()

    @classmethod
    def get(cls):
        return cls.value

    @classmethod
    def subscribe(cls, callback: Callable[[], None]) -> int:
        if cls.subscribers is None:
            cls.subscribers = {}
        subscription_tag: int = dpg.generate_uuid()
        cls.subscribers[subscription_tag] = callback
        return subscription_tag

    @classmethod
    def callback(cls):
        if cls.subscribers is None:
            cls.subscribers = {}
        from settings.file_manager import save_settings  # <- TODO: somehow remove it...
        save_settings(0)  # TODO: fix "0" parameter
        for function in list(cls.subscribers.values()):
            try:
                function()
            except Exception:
                traceback.print_exc()


# Settings
class Example(SettingValue):
    value: bool = True
