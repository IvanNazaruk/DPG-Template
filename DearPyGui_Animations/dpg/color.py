from __future__ import annotations

from typing import Annotated, Optional, Self, Sequence

import dearpygui.dearpygui as dpg
from annotated_types import Gt

from ..animator import Animator, Value
from ..tools import math_round


class ColorValue(Value):
    value: Sequence[Optional[int], Optional[int], Optional[int], Optional[int]]

    def __init__(self, value: Sequence[Optional[int], Optional[int], Optional[int], Optional[int]]):
        value = list(value[:4:])
        if len(value) < 4:
            for _ in range(4 - len(value)):
                value.append(None)
        super().__init__(value)  # noqa


class TextColorAnimation(Animator):
    dpg_object: int | str

    def __init__(self, dpg_object: int | str,
                 start_value: Sequence[Optional[int], Optional[int], Optional[int], Optional[int]]):
        self.dpg_object = dpg_object
        super().__init__(ColorValue(start_value))

    def add_point(self, value: Sequence[Optional[int], Optional[int], Optional[int], Optional[int]],
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        return super().add_point(
            ColorValue(value), duration, cubic_bezier
        )

    def set_value(self, value: Sequence[int, int, int, int]):
        dpg.configure_item(self.dpg_object, color=value)

    def __pre_set_value__(self, value: ColorValue):
        color = list(value.value)
        if None in color:
            now_color = dpg.get_item_configuration(self.dpg_object)['color']
            for i in range(len(now_color)):
                if color[i] is None:
                    color[i] = math_round(now_color[i] * 255)
            for i in range(len(color)):
                if color[i] is None:
                    color[i] = 255
        self.set_value(color)
