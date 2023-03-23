import dearpygui.dearpygui as dpg

from ..animator.value import IntValueAnimationABC


class ScrollYAnimation(IntValueAnimationABC):
    def __init__(self, dpg_object: int | str, start_value: int):
        self.dpg_object = dpg_object
        super().__init__(start_value)

    def set_value(self, value: int):
        dpg.set_y_scroll(self.dpg_object, value)
