import traceback
from typing import Any, Callable

import dearpygui.dearpygui as dpg

from DearPyGui_Addons import dpg_callback
from DearPyGui_Addons.dpg_handler import SubscriptionTag
from .main import all_colors, all_styles, CurrentTheme

__all__ = [
    "update_theme_callback",
    "get_theme_style_value", "get_theme_color_value",
    "get_current_theme_style_value", "get_current_theme_color_value",
    "subscribe_color_theme_change", "unsubscribe_color_theme_change",
    "subscribe_style_theme_change", "unsubscribe_style_theme_change"
]

style_theme_subscribers: dict[int, tuple[int, Callable[[Any], None]]] = {}
colors_theme_subscribers: dict[int, tuple[int, Callable[[Any], None]]] = {}


@dpg_callback(sender=True)
def update_theme_callback(percent: float):
    dpg_theme: int
    callback: Callable[[Any], None]
    for dpg_theme, callback in list(colors_theme_subscribers.values()):
        value = get_theme_color_value(dpg_theme)
        if value is not None:
            try:
                callback(value)
            except Exception:
                traceback.print_exc()
            continue

    for dpg_theme, callback in list(style_theme_subscribers.values()):
        value = get_theme_style_value(dpg_theme)
        if value is not None:
            try:
                callback(value)
            except Exception:
                traceback.print_exc()
            continue


def get_theme_style_value(dpg_style: int) -> list[float, float]:
    dpg_object = all_styles.get(dpg_style, None)
    if dpg_object is not None:
        return dpg.get_value(dpg_object)
    raise NameError(f"Theme {dpg_style} not found")


def get_theme_color_value(dpg_style: int) -> list[int, int, int, int]:
    dpg_object = all_colors.get(dpg_style, None)
    if dpg_object is not None:
        return dpg.get_value(dpg_object)
    raise NameError(f"Theme {dpg_style} not found")


def get_current_theme_style_value(dpg_theme: int) -> list[float, float]:
    theme = CurrentTheme.get().value
    value = theme.styles.get(dpg_theme, None)
    if value is not None:
        return value
    raise NameError(f"Theme {dpg_theme} not found")


def get_current_theme_color_value(dpg_theme: int) -> list[int, int, int, int]:
    theme = CurrentTheme.get().value
    value = theme.colors.get(dpg_theme, None)
    if value is not None:
        return value
    raise NameError(f"Theme {dpg_theme} not found")


def subscribe_color_theme_change(dpg_theme: int, callback: Callable[[Any], None]) -> SubscriptionTag:
    subscribe_tag = dpg.generate_uuid()
    colors_theme_subscribers[subscribe_tag] = (dpg_theme, callback)
    callback(get_theme_color_value(dpg_theme))
    return subscribe_tag


def unsubscribe_color_theme_change(*tags: SubscriptionTag):
    for tag in tags:
        if tag is None:
            continue
        if tag in colors_theme_subscribers:
            del colors_theme_subscribers[tag]


def subscribe_style_theme_change(dpg_theme: int, callback: Callable[[Any], None]) -> SubscriptionTag:
    subscribe_tag = dpg.generate_uuid()
    style_theme_subscribers[subscribe_tag] = (dpg_theme, callback)
    try:
        callback(get_theme_style_value(dpg_theme))
    except Exception:
        traceback.print_exc()
    return subscribe_tag


def unsubscribe_style_theme_change(*tags: SubscriptionTag):
    for tag in tags:
        if tag is None:
            continue
        if tag in style_theme_subscribers:
            del style_theme_subscribers[tag]
