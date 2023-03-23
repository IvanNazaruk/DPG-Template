from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING

import dearpygui.dearpygui as dpg

from ..cubic_bezier import bezier
from ..loop import all_animations
from ..tools import math_round

if TYPE_CHECKING:
    from typing import Annotated, Self, Any, TypeVar
    from annotated_types import Ge, Gt


class Value(ABC):
    value: list[float | int | None]

    def __init__(self, value: list[float | int | None]):
        self.value = value
        self.__post_init__()

    def __post_init__(self):
        for i in range(len(self.value)):
            if isinstance(self.value[i], float):
                self.value[i] = math_round(self.value[i])

    def __add__(self, other: Self) -> Self:
        self_values = [*self.value]
        other_values = [*other.value]
        for i in range(len(self_values)):
            if self_values[i] is not None and other_values[i] is not None:
                other_values[i] = self_values[i] + other_values[i]
        return type(self)(other_values)

    def __sub__(self, other: Self) -> Self:
        self_values = [*self.value]
        other_values = [*other.value]
        for i in range(len(self_values)):
            if self_values[i] is not None and other_values[i] is not None:
                other_values[i] = self_values[i] - other_values[i]
        return type(self)(other_values)

    def __mul__(self, other: float) -> Self:
        self_values = [*self.value]
        for i in range(len(self_values)):
            if self_values[i] is not None:
                self_values[i] = self_values[i] * other
        return type(self)(self_values)


if TYPE_CHECKING:
    ValueType = TypeVar('ValueType', bound=Value)


@dataclass
class Point:
    value: ValueType
    duration: Annotated[float, Gt(0)]
    bezier: Sequence[float, float, float, float] | bezier

    def __post_init__(self):
        self.bezier = bezier(*self.bezier)


@dataclass
class PausePoint:
    value: ValueType  # past point value
    duration: Annotated[float, Gt(0)]
    bezier: Sequence[float, float, float, float] | bezier = None

    def __post_init__(self):
        self.bezier = bezier(0, 0, 1, 1)


class Animator(ABC):
    __id: int
    _deleted: bool

    start_time: float = 0
    __PAUSED: bool
    REVERSED = False
    points: list[Point | PausePoint]
    now_point: int = 0

    time_shift: float = 0

    start_value: ValueType
    end_value: ValueType

    @property
    def PAUSED(self) -> bool:
        return self.__PAUSED

    @PAUSED.setter
    def PAUSED(self, value: bool):
        if self._deleted:
            value = True
        self.__PAUSED = value
        if value:
            if self.__id in all_animations:
                del all_animations[self.__id]
        else:
            all_animations[self.__id] = self  # noqa

    def __init__(self, start_value: ValueType):
        self.points = []
        self.__id = dpg.generate_uuid()
        self._deleted = False
        self.PAUSED = True
        self.start_value = start_value

    @abstractmethod
    def add_point(self, value: ValueType,
                  duration: Annotated[float, Gt(0)],
                  cubic_bezier: Sequence[float, float, float, float] = (0, 0, 1, 1)) -> Self:
        self.end_value = value
        self.points.append(
            Point(value, duration, cubic_bezier)
        )
        return self

    @abstractmethod
    def set_value(self, value: Any):
        ...

    def __pre_set_value__(self, value: ValueType):
        self.set_value(value.value)

    def add_pause_point(self, duration: Annotated[float, Gt(0)]) -> Self:
        if len(self.points) == 0:
            value = self.start_value
        else:
            value = self.points[-1].value
        self.points.append(PausePoint(value, duration))
        return self

    def set_point(self, index: Annotated[int, Ge(0)]) -> Self:
        if index >= len(self.points):
            index = len(self.points) - 1
        elif index < 0:
            index = 0
        self.now_point = index
        self.start_time = time.time()
        return self

    def get_from_point_value(self):
        if self.REVERSED:
            return self.points[self.now_point].value

        point_index = self.now_point - 1
        if point_index < 0:
            return self.start_value
        if point_index >= len(self.points):
            return self.end_value
        return self.points[point_index].value

    def get_future_point_value(self):
        if not self.REVERSED:
            return self.points[self.now_point].value

        point_index = self.now_point - 1
        if point_index < 0:
            return self.start_value
        if point_index >= len(self.points):
            return self.end_value
        return self.points[point_index].value

    def _update(self) -> float | None:
        if self.PAUSED:
            return
        if self._deleted:
            return
        self.time_shift = time.time() - self.start_time
        while True:
            point = self.points[self.now_point]
            if self.time_shift >= point.duration:
                self.__pre_set_value__(self.get_future_point_value())
                self.time_shift -= point.duration
                self.start_time += point.duration
                if self.REVERSED:
                    self.now_point -= 1
                else:
                    self.now_point += 1
                if self.now_point < 0 or self.now_point >= len(self.points):
                    self.PAUSED = True
                    self.now_point = 0
                    return
                continue
            break

        if self.REVERSED:
            return (point.duration - self.time_shift) / point.duration
        return self.time_shift / point.duration

    def update(self) -> Self:
        progress_percent = self._update()
        if progress_percent is None:
            return self
        point = self.points[self.now_point]

        progress_percent: float = point.bezier(progress_percent)

        old_value = self.get_from_point_value()
        new_value = self.get_future_point_value()
        if self.REVERSED:
            old_value, new_value = new_value, old_value

        difference = old_value - new_value
        new_value: ValueType = new_value + difference - (difference * progress_percent)
        self.__pre_set_value__(new_value)
        return self

    def start(self) -> Self:
        if len(self.points) == 0:
            raise ValueError("No points to start. Use `.add_point` to add points")
        self.PAUSED = False
        self.start_time = time.time()
        if self.REVERSED:
            self.now_point = len(self.points) - 1
        else:
            self.now_point = 0
        return self

    def continue_or_start(self) -> Self:
        if self.PAUSED:
            self.start()
        return self

    def set_reverse(self, reverse: bool) -> Self:
        self.REVERSED = reverse
        point = self.points[self.now_point]
        if self.PAUSED:
            self.time_shift = point.duration - self.time_shift
            return self
        self.start_time = time.time() - (point.duration - self.time_shift)
        # self.update()
        return self

    def reverse(self) -> Self:
        self.set_reverse(not self.REVERSED)
        return self

    def resume(self) -> Self:
        self.PAUSED = False
        self.start_time = time.time() - self.time_shift
        return self

    def pause(self) -> Self:
        self.update()
        self.PAUSED = True
        return self

    def delete(self):
        self.PAUSED = True
        self._deleted = True

    def __del__(self):
        self.delete()
