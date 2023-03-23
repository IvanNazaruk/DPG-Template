# Author: dev0-1
from __future__ import annotations

from typing import Optional, Sequence

import dearpygui.dearpygui as dpg

name = """Unreal"""
styles: dict[int, Sequence[float]] = {
    dpg.mvStyleVar_Alpha: [1.0],
    dpg.mvStyleVar_WindowPadding: [8.0, 8.0],
    dpg.mvStyleVar_WindowRounding: [0.0],
    dpg.mvStyleVar_WindowBorderSize: [1.0],
    dpg.mvStyleVar_WindowMinSize: [32.0, 32.0],
    dpg.mvStyleVar_WindowTitleAlign: [0.0, 0.5],
    dpg.mvStyleVar_ChildRounding: [0.0],
    dpg.mvStyleVar_ChildBorderSize: [1.0],
    dpg.mvStyleVar_PopupRounding: [0.0],
    dpg.mvStyleVar_PopupBorderSize: [1.0],
    dpg.mvStyleVar_FramePadding: [4.0, 3.0],
    dpg.mvStyleVar_FrameRounding: [0.0],
    dpg.mvStyleVar_FrameBorderSize: [0.0],
    dpg.mvStyleVar_ItemSpacing: [8.0, 4.0],
    dpg.mvStyleVar_ItemInnerSpacing: [4.0, 4.0],
    dpg.mvStyleVar_CellPadding: [4.0, 2.0],
    dpg.mvStyleVar_IndentSpacing: [21.0],
    dpg.mvStyleVar_ScrollbarSize: [14.0],
    dpg.mvStyleVar_ScrollbarRounding: [9.0],
    dpg.mvStyleVar_GrabMinSize: [10.0],
    dpg.mvStyleVar_GrabRounding: [0.0],
    dpg.mvStyleVar_TabRounding: [4.0],
    dpg.mvStyleVar_ButtonTextAlign: [0.5, 0.5],
    dpg.mvStyleVar_SelectableTextAlign: [0.0, 0.0],
}
colors: dict[int, Sequence[int, int, int, Optional[int]]] = {
    dpg.mvThemeCol_Text: [255, 255, 255, 255],
    dpg.mvThemeCol_TextDisabled: [127, 127, 127, 255],
    dpg.mvThemeCol_WindowBg: [15, 15, 15, 239],
    dpg.mvThemeCol_ChildBg: [15, 15, 15, 239],
    dpg.mvThemeCol_PopupBg: [15, 15, 15, 239],
    dpg.mvThemeCol_Border: [109, 109, 127, 127],
    dpg.mvThemeCol_BorderShadow: [0, 0, 0, 0],
    dpg.mvThemeCol_FrameBg: [51, 53, 56, 137],
    dpg.mvThemeCol_FrameBgHovered: [102, 102, 102, 102],
    dpg.mvThemeCol_FrameBgActive: [45, 45, 45, 170],
    dpg.mvThemeCol_TitleBg: [10, 10, 10, 255],
    dpg.mvThemeCol_TitleBgActive: [73, 73, 73, 255],
    dpg.mvThemeCol_TitleBgCollapsed: [0, 0, 0, 130],
    dpg.mvThemeCol_MenuBarBg: [35, 35, 35, 255],
    dpg.mvThemeCol_ScrollbarBg: [5, 5, 5, 135],
    dpg.mvThemeCol_ScrollbarGrab: [79, 79, 79, 255],
    dpg.mvThemeCol_ScrollbarGrabHovered: [104, 104, 104, 255],
    dpg.mvThemeCol_ScrollbarGrabActive: [130, 130, 130, 255],
    dpg.mvThemeCol_CheckMark: [239, 239, 239, 255],
    dpg.mvThemeCol_SliderGrab: [130, 130, 130, 255],
    dpg.mvThemeCol_SliderGrabActive: [219, 219, 219, 255],
    dpg.mvThemeCol_Button: [112, 112, 112, 102],
    dpg.mvThemeCol_ButtonHovered: [117, 119, 122, 255],
    dpg.mvThemeCol_ButtonActive: [107, 107, 107, 255],
    dpg.mvThemeCol_Header: [178, 178, 178, 79],
    dpg.mvThemeCol_HeaderHovered: [178, 178, 178, 204],
    dpg.mvThemeCol_HeaderActive: [122, 127, 132, 255],
    dpg.mvThemeCol_Separator: [109, 109, 127, 127],
    dpg.mvThemeCol_SeparatorHovered: [183, 183, 183, 198],
    dpg.mvThemeCol_SeparatorActive: [130, 130, 130, 255],
    dpg.mvThemeCol_ResizeGrip: [232, 232, 232, 63],
    dpg.mvThemeCol_ResizeGripHovered: [206, 206, 206, 170],
    dpg.mvThemeCol_ResizeGripActive: [117, 117, 117, 242],
    dpg.mvThemeCol_Tab: [45, 89, 147, 219],
    dpg.mvThemeCol_TabHovered: [66, 150, 249, 204],
    dpg.mvThemeCol_TabActive: [50, 104, 173, 255],
    dpg.mvThemeCol_TabUnfocused: [17, 26, 37, 247],
    dpg.mvThemeCol_TabUnfocusedActive: [34, 66, 108, 255],
    dpg.mvThemeCol_PlotLines: [155, 155, 155, 255],
    dpg.mvThemeCol_PlotLinesHovered: [255, 109, 89, 255],
    dpg.mvThemeCol_PlotHistogram: [186, 153, 38, 255],
    dpg.mvThemeCol_PlotHistogramHovered: [255, 153, 0, 255],
    dpg.mvThemeCol_TableHeaderBg: [48, 48, 51, 255],
    dpg.mvThemeCol_TableBorderStrong: [79, 79, 89, 255],
    dpg.mvThemeCol_TableBorderLight: [58, 58, 63, 255],
    dpg.mvThemeCol_TableRowBg: [0, 0, 0, 0],
    dpg.mvThemeCol_TableRowBgAlt: [255, 255, 255, 15],
    dpg.mvThemeCol_TextSelectedBg: [221, 221, 221, 89],
    dpg.mvThemeCol_DragDropTarget: [255, 255, 0, 229],
    dpg.mvThemeCol_NavHighlight: [153, 153, 153, 255],
    dpg.mvThemeCol_NavWindowingHighlight: [255, 255, 255, 178],
    dpg.mvThemeCol_NavWindowingDimBg: [204, 204, 204, 51],
    dpg.mvThemeCol_ModalWindowDimBg: [204, 204, 204, 89],
}
