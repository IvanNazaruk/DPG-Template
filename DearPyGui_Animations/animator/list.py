from __future__ import annotations

import traceback
from abc import ABC, abstractmethod
from typing import Callable, Self, Sequence, TYPE_CHECKING

from . import Animator, Value

if TYPE_CHECKING:
    from typing import Annotated
    from annotated_types import Gt


class IntListValues(Value):
    value: list[int]


class IntListAnimationABC(Animator, ABC):
    def __init__(self, start_value: list[int]):
        super().__init__(IntListValues(start_value))

    def add_point(self, value: list[int],
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        return super().add_point(
            IntListValues(value), duration, cubic_bezier
        )

    @abstractmethod
    def set_value(self, value: list[int]):
        ...


class IntListAnimation(IntListAnimationABC):
    set_value_callback: Callable[[list[int]], None] | None

    def __init__(self, start_value: list[int],
                 set_value_callback: Callable[[list[int]], None] = None):
        self.set_value_callback = set_value_callback
        super().__init__(start_value)

    def set_value(self, value: list[int]):
        if self.set_value_callback:
            try:
                self.set_value_callback(value)
            except Exception:
                traceback.print_exc()


class FloatListValues(Value):
    value: list[float]

    def __post_init__(self): pass


class FloatListAnimationABC(Animator, ABC):
    def __init__(self, start_value: list[float]):
        super().__init__(IntListValues(start_value))

    def add_point(self, value: list[float],
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        return super().add_point(
            FloatListValues(value), duration, cubic_bezier
        )

    @abstractmethod
    def set_value(self, value: list[float]):
        ...


class FloatListAnimation(FloatListAnimationABC):
    set_value_callback: Callable[[list[float]], None] | None

    def __init__(self, start_value: list[float],
                 set_value_callback: Callable[[list[float]], None] = None):
        self.set_value_callback = set_value_callback
        super().__init__(start_value)

    def set_value(self, value: list[float]):
        if self.set_value_callback:
            try:
                self.set_value_callback(value)
            except Exception:
                traceback.print_exc()
