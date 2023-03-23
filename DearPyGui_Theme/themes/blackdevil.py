# Author: Naeemullah1
from __future__ import annotations

from typing import Optional, Sequence

import dearpygui.dearpygui as dpg

name = """BlackDevil"""
styles: dict[int, Sequence[float]] = {
    dpg.mvStyleVar_Alpha: [1.0],
    dpg.mvStyleVar_WindowPadding: [10.0, 10.0],
    dpg.mvStyleVar_WindowRounding: [5.0],
    dpg.mvStyleVar_WindowBorderSize: [1.0],
    dpg.mvStyleVar_WindowMinSize: [20.0, 20.0],
    dpg.mvStyleVar_WindowTitleAlign: [0.0, 0.5],
    dpg.mvStyleVar_ChildRounding: [5.0],
    dpg.mvStyleVar_ChildBorderSize: [1.0],
    dpg.mvStyleVar_PopupRounding: [5.0],
    dpg.mvStyleVar_PopupBorderSize: [1.0],
    dpg.mvStyleVar_FramePadding: [5.0, 5.0],
    dpg.mvStyleVar_FrameRounding: [5.0],
    dpg.mvStyleVar_FrameBorderSize: [0.0],
    dpg.mvStyleVar_ItemSpacing: [8.0, 5.0],
    dpg.mvStyleVar_ItemInnerSpacing: [5.0, 5.0],
    dpg.mvStyleVar_CellPadding: [5.0, 5.0],
    dpg.mvStyleVar_IndentSpacing: [10.0],
    dpg.mvStyleVar_ScrollbarSize: [10.0],
    dpg.mvStyleVar_ScrollbarRounding: [5.0],
    dpg.mvStyleVar_GrabMinSize: [10.0],
    dpg.mvStyleVar_GrabRounding: [0.0],
    dpg.mvStyleVar_TabRounding: [10.0],
    dpg.mvStyleVar_ButtonTextAlign: [0.5, 0.5],
    dpg.mvStyleVar_SelectableTextAlign: [0.0, 0.0],
}
colors: dict[int, Sequence[int, int, int, Optional[int]]] = {
    dpg.mvThemeCol_Text: [200, 200, 200, 255],
    dpg.mvThemeCol_TextDisabled: [111, 104, 80, 255],
    dpg.mvThemeCol_WindowBg: [15, 30, 15, 100],
    dpg.mvThemeCol_ChildBg: [15, 30, 15, 100],
    dpg.mvThemeCol_PopupBg: [15, 30, 15, 100],
    dpg.mvThemeCol_Border: [100, 0, 0, 200],
    dpg.mvThemeCol_BorderShadow: [0, 0, 0, 0],
    dpg.mvThemeCol_FrameBg: [15, 30, 40, 200],
    dpg.mvThemeCol_FrameBgHovered: [30, 60, 90, 200],
    dpg.mvThemeCol_FrameBgActive: [90, 90, 30, 200],
    dpg.mvThemeCol_TitleBg: [15, 30, 40, 200],
    dpg.mvThemeCol_TitleBgActive: [15, 30, 40, 200],
    dpg.mvThemeCol_TitleBgCollapsed: [15, 30, 40, 50],
    dpg.mvThemeCol_MenuBarBg: [20, 20, 20, 200],
    dpg.mvThemeCol_ScrollbarBg: [15, 30, 40, 200],
    dpg.mvThemeCol_ScrollbarGrab: [30, 90, 60, 200],
    dpg.mvThemeCol_ScrollbarGrabHovered: [30, 90, 90, 200],
    dpg.mvThemeCol_ScrollbarGrabActive: [30, 150, 60, 200],
    dpg.mvThemeCol_CheckMark: [30, 150, 60, 200],
    dpg.mvThemeCol_SliderGrab: [30, 90, 60, 200],
    dpg.mvThemeCol_SliderGrabActive: [30, 150, 60, 200],
    dpg.mvThemeCol_Button: [90, 90, 30, 200],
    dpg.mvThemeCol_ButtonHovered: [90, 120, 60, 200],
    dpg.mvThemeCol_ButtonActive: [150, 90, 60, 200],
    dpg.mvThemeCol_Header: [15, 30, 40, 200],
    dpg.mvThemeCol_HeaderHovered: [30, 90, 90, 200],
    dpg.mvThemeCol_HeaderActive: [30, 150, 60, 200],
    dpg.mvThemeCol_Separator: [90, 90, 60, 200],
    dpg.mvThemeCol_SeparatorHovered: [30, 90, 90, 200],
    dpg.mvThemeCol_SeparatorActive: [150, 90, 60, 200],
    dpg.mvThemeCol_ResizeGrip: [15, 30, 40, 200],
    dpg.mvThemeCol_ResizeGripHovered: [150, 90, 90, 200],
    dpg.mvThemeCol_ResizeGripActive: [150, 60, 60, 200],
    dpg.mvThemeCol_Tab: [90, 90, 30, 200],
    dpg.mvThemeCol_TabHovered: [90, 120, 60, 200],
    dpg.mvThemeCol_TabActive: [150, 90, 60, 200],
    dpg.mvThemeCol_TabUnfocused: [15, 30, 40, 200],
    dpg.mvThemeCol_TabUnfocusedActive: [150, 90, 90, 200],
    dpg.mvThemeCol_PlotLines: [100, 200, 100, 200],
    dpg.mvThemeCol_PlotLinesHovered: [255, 109, 89, 200],
    dpg.mvThemeCol_PlotHistogram: [0, 90, 100, 200],
    dpg.mvThemeCol_PlotHistogramHovered: [50, 150, 150, 200],
    dpg.mvThemeCol_TableHeaderBg: [48, 48, 51, 200],
    dpg.mvThemeCol_TableBorderStrong: [79, 79, 89, 200],
    dpg.mvThemeCol_TableBorderLight: [58, 58, 63, 200],
    dpg.mvThemeCol_TableRowBg: [0, 0, 0, 200],
    dpg.mvThemeCol_TableRowBgAlt: [255, 255, 255, 15],
    dpg.mvThemeCol_TextSelectedBg: [100, 90, 100, 100],
    dpg.mvThemeCol_DragDropTarget: [255, 255, 0, 229],
    dpg.mvThemeCol_NavHighlight: [66, 150, 249, 255],
    dpg.mvThemeCol_NavWindowingHighlight: [255, 255, 255, 178],
    dpg.mvThemeCol_NavWindowingDimBg: [204, 204, 204, 51],
    dpg.mvThemeCol_ModalWindowDimBg: [204, 204, 204, 89],
}
