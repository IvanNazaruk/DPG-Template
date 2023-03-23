from __future__ import annotations

from typing import Annotated, Optional, Self, Sequence

import dearpygui.dearpygui as dpg
from annotated_types import Gt

from .color import TextColorAnimation
from ..animator import Animator, Value


class StyleColorAnimation(TextColorAnimation):
    def set_value(self, value: Sequence[int, int, int, int]):
        dpg.set_value(self.dpg_object, value)


class StyleValue(Value):
    value: Sequence[Optional[float], Optional[float]]

    def __init__(self, value: Sequence[Optional[float], Optional[float]]):
        value = list(value[:2:])
        if len(value) < 2:
            for _ in range(2 - len(value)):
                value.append(None)
        super().__init__(value)  # noqa

    def __post_init__(self):
        pass


class StyleAnimation(Animator):
    dpg_object: int | str

    def __init__(self, dpg_object: int | str,
                 start_value: Sequence[Optional[float], Optional[float]]):
        self.dpg_object = dpg_object
        super().__init__(StyleValue(start_value))

    def add_point(self, value: Sequence[Optional[float], Optional[float]],
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        return super().add_point(
            StyleValue(value), duration, cubic_bezier
        )

    def set_value(self, value: Sequence[float, float]):
        dpg.set_value(self.dpg_object, value)

    def __pre_set_value__(self, value: StyleValue):
        style = list(value.value)
        if None in style:
            now_style = dpg.get_value(self.dpg_object)
            for i in range(len(now_style)):
                if style[i] is None:
                    style[i] = now_style[i]
            for i in range(len(style)):
                if style[i] is None:
                    style[i] = -1
        self.set_value(style)
