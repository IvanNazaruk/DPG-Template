# Author: usernameiwantedwasalreadytaken
from __future__ import annotations

from typing import Optional, Sequence

import dearpygui.dearpygui as dpg

name = """Microsoft"""
styles: dict[int, Sequence[float]] = {
    dpg.mvStyleVar_Alpha: [1.0],
    dpg.mvStyleVar_WindowPadding: [4.0, 6.0],
    dpg.mvStyleVar_WindowRounding: [0.0],
    dpg.mvStyleVar_WindowBorderSize: [0.0],
    dpg.mvStyleVar_WindowMinSize: [32.0, 32.0],
    dpg.mvStyleVar_WindowTitleAlign: [0.0, 0.5],
    dpg.mvStyleVar_ChildRounding: [0.0],
    dpg.mvStyleVar_ChildBorderSize: [1.0],
    dpg.mvStyleVar_PopupRounding: [0.0],
    dpg.mvStyleVar_PopupBorderSize: [1.0],
    dpg.mvStyleVar_FramePadding: [8.0, 6.0],
    dpg.mvStyleVar_FrameRounding: [0.0],
    dpg.mvStyleVar_FrameBorderSize: [1.0],
    dpg.mvStyleVar_ItemSpacing: [8.0, 6.0],
    dpg.mvStyleVar_ItemInnerSpacing: [8.0, 6.0],
    dpg.mvStyleVar_CellPadding: [4.0, 2.0],
    dpg.mvStyleVar_IndentSpacing: [20.0],
    dpg.mvStyleVar_ScrollbarSize: [20.0],
    dpg.mvStyleVar_ScrollbarRounding: [0.0],
    dpg.mvStyleVar_GrabMinSize: [5.0],
    dpg.mvStyleVar_GrabRounding: [0.0],
    dpg.mvStyleVar_TabRounding: [4.0],
    dpg.mvStyleVar_ButtonTextAlign: [0.5, 0.5],
    dpg.mvStyleVar_SelectableTextAlign: [0.0, 0.0],
}
colors: dict[int, Sequence[int, int, int, Optional[int]]] = {
    dpg.mvThemeCol_Text: [25, 25, 25, 255],
    dpg.mvThemeCol_TextDisabled: [127, 127, 127, 255],
    dpg.mvThemeCol_WindowBg: [242, 242, 242, 255],
    dpg.mvThemeCol_ChildBg: [242, 242, 242, 255],
    dpg.mvThemeCol_PopupBg: [242, 242, 242, 255],
    dpg.mvThemeCol_Border: [153, 153, 153, 255],
    dpg.mvThemeCol_BorderShadow: [0, 0, 0, 0],
    dpg.mvThemeCol_FrameBg: [255, 255, 255, 255],
    dpg.mvThemeCol_FrameBgHovered: [0, 119, 214, 51],
    dpg.mvThemeCol_FrameBgActive: [0, 119, 214, 255],
    dpg.mvThemeCol_TitleBg: [10, 10, 10, 255],
    dpg.mvThemeCol_TitleBgActive: [40, 73, 122, 255],
    dpg.mvThemeCol_TitleBgCollapsed: [0, 0, 0, 130],
    dpg.mvThemeCol_MenuBarBg: [219, 219, 219, 255],
    dpg.mvThemeCol_ScrollbarBg: [219, 219, 219, 255],
    dpg.mvThemeCol_ScrollbarGrab: [175, 175, 175, 255],
    dpg.mvThemeCol_ScrollbarGrabHovered: [0, 0, 0, 51],
    dpg.mvThemeCol_ScrollbarGrabActive: [0, 0, 0, 127],
    dpg.mvThemeCol_CheckMark: [25, 25, 25, 255],
    dpg.mvThemeCol_SliderGrab: [175, 175, 175, 255],
    dpg.mvThemeCol_SliderGrabActive: [0, 0, 0, 127],
    dpg.mvThemeCol_Button: [219, 219, 219, 255],
    dpg.mvThemeCol_ButtonHovered: [0, 119, 214, 51],
    dpg.mvThemeCol_ButtonActive: [0, 119, 214, 255],
    dpg.mvThemeCol_Header: [219, 219, 219, 255],
    dpg.mvThemeCol_HeaderHovered: [0, 119, 214, 51],
    dpg.mvThemeCol_HeaderActive: [0, 119, 214, 255],
    dpg.mvThemeCol_Separator: [109, 109, 127, 127],
    dpg.mvThemeCol_SeparatorHovered: [25, 102, 191, 198],
    dpg.mvThemeCol_SeparatorActive: [25, 102, 191, 255],
    dpg.mvThemeCol_ResizeGrip: [66, 150, 249, 51],
    dpg.mvThemeCol_ResizeGripHovered: [66, 150, 249, 170],
    dpg.mvThemeCol_ResizeGripActive: [66, 150, 249, 242],
    dpg.mvThemeCol_Tab: [45, 89, 147, 219],
    dpg.mvThemeCol_TabHovered: [66, 150, 249, 204],
    dpg.mvThemeCol_TabActive: [50, 104, 173, 255],
    dpg.mvThemeCol_TabUnfocused: [17, 26, 37, 247],
    dpg.mvThemeCol_TabUnfocusedActive: [34, 66, 108, 255],
    dpg.mvThemeCol_PlotLines: [155, 155, 155, 255],
    dpg.mvThemeCol_PlotLinesHovered: [255, 109, 89, 255],
    dpg.mvThemeCol_PlotHistogram: [229, 178, 0, 255],
    dpg.mvThemeCol_PlotHistogramHovered: [255, 153, 0, 255],
    dpg.mvThemeCol_TableHeaderBg: [48, 48, 51, 255],
    dpg.mvThemeCol_TableBorderStrong: [79, 79, 89, 255],
    dpg.mvThemeCol_TableBorderLight: [58, 58, 63, 255],
    dpg.mvThemeCol_TableRowBg: [0, 0, 0, 0],
    dpg.mvThemeCol_TableRowBgAlt: [255, 255, 255, 15],
    dpg.mvThemeCol_TextSelectedBg: [66, 150, 249, 89],
    dpg.mvThemeCol_DragDropTarget: [255, 255, 0, 229],
    dpg.mvThemeCol_NavHighlight: [66, 150, 249, 255],
    dpg.mvThemeCol_NavWindowingHighlight: [255, 255, 255, 178],
    dpg.mvThemeCol_NavWindowingDimBg: [204, 204, 204, 51],
    dpg.mvThemeCol_ModalWindowDimBg: [204, 204, 204, 89],
}
