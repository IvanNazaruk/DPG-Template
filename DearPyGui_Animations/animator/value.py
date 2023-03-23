from __future__ import annotations

import traceback
from abc import ABC, abstractmethod
from typing import Annotated, Callable, Self, Sequence

from annotated_types import Gt

from . import Animator, Value
from ..tools import math_round


class IntValue(Value):
    value: int

    def __init__(self, value: int | float):
        super().__init__(value)  # noqa

    def __post_init__(self):
        if isinstance(self.value, float):
            self.value = math_round(self.value)

    def __add__(self, other: Self) -> Self:
        return type(self)(self.value + other.value)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.value - other.value)

    def __mul__(self, other: float) -> Self:
        return type(self)(self.value * other)


class IntValueAnimationABC(Animator, ABC):
    def __init__(self, start_value: int):
        super().__init__(IntValue(start_value))

    def add_point(self, value: int,
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        return super().add_point(
            IntValue(value), duration, cubic_bezier
        )

    @abstractmethod
    def set_value(self, value: int):
        ...


class IntValueAnimation(IntValueAnimationABC):
    set_value_callback: Callable[[int], None] | None

    def __init__(self, start_value: int,
                 set_value_callback: Callable[[int], None] = None):
        self.set_value_callback = set_value_callback
        super().__init__(start_value)

    def set_value(self, value: int):
        if self.set_value_callback:
            try:
                self.set_value_callback(value)
            except Exception:
                traceback.print_exc()


class FloatValue(IntValue):
    value: float

    def __init__(self, value: float):
        super().__init__(value)  # noqa

    def __post_init__(self): pass


class FloatValueAnimationABC(Animator, ABC):
    def __init__(self, start_value: float):
        super().__init__(FloatValue(start_value))

    def add_point(self, value: float,
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        return super().add_point(
            FloatValue(value), duration, cubic_bezier
        )

    @abstractmethod
    def set_value(self, value: float):
        ...


class FloatValueAnimation(FloatValueAnimationABC):
    set_value_callback: Callable[[float], None] | None

    def __init__(self, start_value: float,
                 set_value_callback: Callable[[float], None] = None):
        self.set_value_callback = set_value_callback
        super().__init__(start_value)

    def set_value(self, value: float):
        if self.set_value_callback:
            try:
                self.set_value_callback(value)
            except Exception:
                traceback.print_exc()
