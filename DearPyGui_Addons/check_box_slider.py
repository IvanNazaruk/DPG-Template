from __future__ import annotations

import traceback
from typing import Any, Callable, Optional, Self

import dearpygui.dearpygui as dpg

import DearPyGui_Theme as dpg_theme
import fonts
from DearPyGui_Animations import PosAnimation, TextColorAnimation
from DearPyGui_Animations.dpg.position import PosValue
from .dpg_callback import dpg_callback
from .handler_deleter import HandlerDeleter


class CheckBoxAnimation(PosAnimation):
    def set_value(self, value: list[int, int]):
        dpg.configure_item(self.dpg_object, center=value)

    def __pre_set_value__(self, value: PosValue):
        pos = list(value.value)
        if None in pos:
            now_pos = dpg.get_item_configuration(self.dpg_object)['center']
            for i in range(len(now_pos)):
                if pos[i] is None:
                    pos[i] = now_pos[i]
            for i in range(len(pos)):
                if pos[i] is None:
                    pos[i] = 0
        self.set_value(pos)


class CheckBoxColorAnimation(TextColorAnimation):
    def set_value(self, value: list[int, int, int, int]):
        dpg.configure_item(self.dpg_object, fill=value)


class _CheckBoxSlider:
    VALUE: bool = True

    WIDTH: int = 40
    HEIGHT: int = 20

    BACKGROUND_COLOR = (32, 30, 33)
    ACTIVE_COLOR = (46, 255, 192)
    INACTIVE_COLOR = (27, 59, 49)

    ANIMATION_DURATION = 0.35

    group: int | None = None
    __handler: int | None
    pos_animation: CheckBoxAnimation = None
    color_animation: CheckBoxColorAnimation = None

    background_objects: list

    __theme: int = None

    @classmethod
    def __get_theme(cls):
        if cls.__theme is None:
            with dpg.theme() as cls.__theme:
                with dpg.theme_component(dpg.mvAll) as theme_component:
                    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)
                    dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0, 0, category=dpg.mvThemeCat_Core, parent=theme_component)

        return cls.__theme

    def __init__(self, callback: Callable[[bool], Any] = None):
        self.background_objects = []
        with dpg.item_handler_registry() as self.__handler:
            self.__click_handler = dpg.add_item_clicked_handler(callback=self.on_click)
        self.callback = callback

    def _update_status(self):
        self.pos_animation.set_reverse(not self.VALUE)
        self.pos_animation.continue_or_start()
        self.color_animation.set_reverse(not self.VALUE)
        self.color_animation.continue_or_start()

    def set_enabled(self, enabled: bool):
        dpg.configure_item(self.__click_handler, show=enabled)

    def get_value(self) -> bool:
        return self.VALUE

    def set_value(self, value: bool):
        if value == self.VALUE:
            return
        self.VALUE = value
        self._update_status()

    def create(self, value: bool = True) -> Self:
        self.VALUE = value
        self.delete(recreate=True)
        with dpg.group() as self.group:
            with dpg.group(horizontal=True, parent=self.group) as theme_group:
                dpg.bind_item_theme(theme_group, self.__get_theme())
                with dpg.group(parent=theme_group) as group:
                    with dpg.drawlist(width=self.WIDTH, height=self.HEIGHT, parent=group) as drawlist:
                        circle_radius = self.HEIGHT / 2

                        # Background
                        _1 = dpg.draw_circle([circle_radius, circle_radius], circle_radius,
                                             fill=self.BACKGROUND_COLOR, color=self.BACKGROUND_COLOR, parent=drawlist)
                        _2 = dpg.draw_quad([circle_radius, 0],
                                           [self.WIDTH - circle_radius, 0], [self.WIDTH - circle_radius, self.HEIGHT],
                                           [circle_radius, self.HEIGHT],
                                           fill=self.BACKGROUND_COLOR, color=self.BACKGROUND_COLOR)
                        _3 = dpg.draw_circle([self.WIDTH - circle_radius, circle_radius], circle_radius,
                                             fill=self.BACKGROUND_COLOR, color=self.BACKGROUND_COLOR, parent=drawlist)
                        self.background_objects.extend([_1, _2, _3])
                        # Foreground
                        # FOREGROUND_COLOR = self.ACTIVE_COLOR if self.VALUE else self.INACTIVE_COLOR
                        FOREGROUND_COLOR = self.INACTIVE_COLOR
                        foreground_circle_radius = circle_radius * 0.6
                        foreground_circle = dpg.draw_circle([circle_radius, circle_radius], foreground_circle_radius,
                                                            fill=FOREGROUND_COLOR, color=[0, 0, 0, 0],
                                                            thickness=0, parent=drawlist)

                        # Animations
                        circle_radius = int(circle_radius)
                        self.pos_animation = CheckBoxAnimation(foreground_circle, [circle_radius, circle_radius]) \
                            .add_point([self.WIDTH - circle_radius, circle_radius], self.ANIMATION_DURATION, (.55, -0.01, .4, 1))
                        self.color_animation = CheckBoxColorAnimation(foreground_circle, self.INACTIVE_COLOR) \
                            .add_point(self.ACTIVE_COLOR, self.ANIMATION_DURATION, (.55, -0.01, .4, 1))
                        self._update_status()
                    dpg.bind_item_handler_registry(drawlist, self.__handler)
        return self

    @dpg_callback()
    def on_click(self):
        self.VALUE = not self.VALUE
        self._update_status()
        if self.callback:
            self.callback(self.VALUE)

    def __del__(self):
        self.delete()

    def delete(self, *, recreate: bool = False):
        self.background_objects = []
        if self.pos_animation:
            self.pos_animation.delete()
        if self.color_animation:
            self.color_animation.delete()
        try:
            dpg.delete_item(self.group, children_only=recreate)
        except Exception:
            pass
        finally:
            self.group = None
        self.pos_animation = None  # noqa
        self.color_animation = None  # noqa

        if recreate and self.__handler is None:
            with dpg.item_handler_registry() as self.__handler:
                dpg.add_item_clicked_handler(callback=self.on_click)
        if not recreate:
            HandlerDeleter.add(self.__handler)
            self.__handler = None


class ThemeCheckBoxSlider(_CheckBoxSlider):
    WIDTH = fonts.font_size * 2
    HEIGHT = fonts.font_size

    # BACKGROUND_COLOR = dpg.mvThemeCol_FrameBg
    # ACTIVE_COLOR = dpg.mvThemeCol_Text
    # INACTIVE_COLOR = dpg.mvThemeCol_Text

    bg_color_theme_change_tag: int | None = None
    fg_color_theme_change_tag: int | None = None
    fp_style_theme_change_tag: int | None = None
    horizontal_frame_padding_objects: tuple[int, int] | None = None
    vertical_frame_padding_objects: tuple[int, int] | None = None

    def _update_foreground_color(self, color: list[int, int, int, Optional[int]]):
        color = color[:3:]
        self.ACTIVE_COLOR = color + [255]
        self.INACTIVE_COLOR = color + [125]

        if self.color_animation:
            end_point = self.color_animation.points[0]
            end_point.value = type(end_point.value)(self.ACTIVE_COLOR)
            self.color_animation.start_value = type(self.color_animation.start_value)(self.INACTIVE_COLOR)
            if self.color_animation.PAUSED:
                value = end_point.value if self.VALUE else self.color_animation.start_value
                self.color_animation.__pre_set_value__(value)
            else:
                self.color_animation.update()

    def _update_background_color(self, color: list[int, int, int, int]):
        bg_color = dpg_theme.get_theme_color_value(dpg.mvThemeCol_WindowBg)
        alpha = color[3] / 255.0
        blend_color = [int((1 - alpha) * bg_color[i] + alpha * color[i]) for i in range(3)]

        self.BACKGROUND_COLOR = blend_color
        for dpg_object in self.background_objects:
            try:
                dpg.configure_item(dpg_object, fill=self.BACKGROUND_COLOR, color=self.BACKGROUND_COLOR)
            except Exception:
                pass

    def _update_frame_padding(self, _):
        if self.horizontal_frame_padding_objects is None or self.vertical_frame_padding_objects is None:
            return

        spacer_width, spacer_height = dpg_theme.get_theme_style_value(dpg.mvStyleVar_FramePadding)
        for horizontal_spacer, vertical_spacer in zip(self.horizontal_frame_padding_objects, self.vertical_frame_padding_objects):
            try:
                dpg.configure_item(horizontal_spacer, width=spacer_width)
            except Exception:
                traceback.print_exc()
            try:
                dpg.configure_item(vertical_spacer, height=spacer_height)
            except Exception:
                traceback.print_exc()

    def create(self, value: bool = True) -> Self:
        super().create(value)
        if self.bg_color_theme_change_tag:
            dpg_theme.unsubscribe_color_theme_change(self.fg_color_theme_change_tag)
        if self.fg_color_theme_change_tag:
            dpg_theme.unsubscribe_color_theme_change(self.fg_color_theme_change_tag)
        self.bg_color_theme_change_tag = dpg_theme.subscribe_color_theme_change(dpg.mvThemeCol_FrameBg, self._update_background_color)
        self.fg_color_theme_change_tag = dpg_theme.subscribe_color_theme_change(dpg.mvThemeCol_Text, self._update_foreground_color)

        horizontal_group = dpg.get_item_children(self.group, 1)[0]
        vertical_group = dpg.get_item_children(horizontal_group, 1)[0]
        _1 = dpg.add_spacer(width=0, height=0, parent=horizontal_group)
        _2 = dpg.add_spacer(width=0, height=0, before=vertical_group)
        self.horizontal_frame_padding_objects = (_1, _2)

        drawlist = dpg.get_item_children(vertical_group, 1)[0]
        _1 = dpg.add_spacer(width=0, height=0, parent=vertical_group)
        _2 = dpg.add_spacer(width=0, height=0, before=drawlist)
        self.vertical_frame_padding_objects = (_1, _2)

        self.fp_style_theme_change_tag = dpg_theme.subscribe_style_theme_change(dpg.mvStyleVar_FramePadding, self._update_frame_padding)
        return self

    def delete(self, *, recreate: bool = False):
        self.horizontal_frame_padding_objects = None
        self.vertical_frame_padding_objects = None
        dpg_theme.unsubscribe_color_theme_change(
            self.bg_color_theme_change_tag,
            self.fg_color_theme_change_tag,
            self.fp_style_theme_change_tag
        )
        self.bg_color_theme_change_tag \
            = self.fg_color_theme_change_tag \
            = self.fp_style_theme_change_tag = None
        super().delete(recreate=recreate)
