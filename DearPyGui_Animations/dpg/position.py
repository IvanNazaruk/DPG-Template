from __future__ import annotations

from typing import Annotated, Optional, Self, Sequence

import dearpygui.dearpygui as dpg
from annotated_types import Gt

from ..animator import Animator, Value


class PosValue(Value):
    value: Sequence[Optional[int], Optional[int]]

    def __init__(self, value: Sequence[Optional[int], Optional[int]]):
        value = list(value[:2:])
        if len(value) < 2:
            for _ in range(2 - len(value)):
                value.append(None)
        super().__init__(value)  # noqa


class PosAnimation(Animator):
    dpg_object: int | str

    def __init__(self, dpg_object: int | str,
                 start_value: Sequence[Optional[int], Optional[int]]):
        self.dpg_object = dpg_object
        super().__init__(PosValue(start_value))

    def add_point(self, value: Sequence[Optional[int], Optional[int]],
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        return super().add_point(
            PosValue(value), duration, cubic_bezier
        )

    def set_value(self, value: Sequence[int, int]):
        dpg.set_item_pos(self.dpg_object, value)  # noqa

    def __pre_set_value__(self, value: PosValue):
        pos = list(value.value)
        if None in pos:
            now_pos = dpg.get_item_pos(self.dpg_object)
            for i in range(len(now_pos)):
                if pos[i] is None:
                    pos[i] = now_pos[i]
            for i in range(len(pos)):
                if pos[i] is None:
                    pos[i] = 0
        self.set_value(pos)
