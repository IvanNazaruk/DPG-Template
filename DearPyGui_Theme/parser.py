# Themes: https://github.com/Patitotective/ImThemes

import os.path
import string
import tomllib

rename: dict[str, str] = {
    # styles
    'alpha': 'dpg.mvStyleVar_Alpha',
    'buttonTextAlign': 'dpg.mvStyleVar_ButtonTextAlign',
    'cellPadding': 'dpg.mvStyleVar_CellPadding',
    'childBorderSize': 'dpg.mvStyleVar_ChildBorderSize',
    'childRounding': 'dpg.mvStyleVar_ChildRounding',
    'frameBorderSize': 'dpg.mvStyleVar_FrameBorderSize',
    'framePadding': 'dpg.mvStyleVar_FramePadding',
    'frameRounding': 'dpg.mvStyleVar_FrameRounding',
    'grabMinSize': 'dpg.mvStyleVar_GrabMinSize',
    'grabRounding': 'dpg.mvStyleVar_GrabRounding',
    'indentSpacing': 'dpg.mvStyleVar_IndentSpacing',
    'itemInnerSpacing': 'dpg.mvStyleVar_ItemInnerSpacing',
    'itemSpacing': 'dpg.mvStyleVar_ItemSpacing',
    'popupBorderSize': 'dpg.mvStyleVar_PopupBorderSize',
    'popupRounding': 'dpg.mvStyleVar_PopupRounding',
    'scrollbarRounding': 'dpg.mvStyleVar_ScrollbarRounding',
    'scrollbarSize': 'dpg.mvStyleVar_ScrollbarSize',
    'selectableTextAlign': 'dpg.mvStyleVar_SelectableTextAlign',
    'tabRounding': 'dpg.mvStyleVar_TabRounding',
    'windowBorderSize': 'dpg.mvStyleVar_WindowBorderSize',
    'windowMinSize': 'dpg.mvStyleVar_WindowMinSize',
    'windowPadding': 'dpg.mvStyleVar_WindowPadding',
    'windowRounding': 'dpg.mvStyleVar_WindowRounding',
    'windowTitleAlign': 'dpg.mvStyleVar_WindowTitleAlign',

    # colors
    'Border': 'dpg.mvThemeCol_Border',
    'BorderShadow': 'dpg.mvThemeCol_BorderShadow',
    'Button': 'dpg.mvThemeCol_Button',
    'ButtonActive': 'dpg.mvThemeCol_ButtonActive',
    'ButtonHovered': 'dpg.mvThemeCol_ButtonHovered',
    'CheckMark': 'dpg.mvThemeCol_CheckMark',
    'DragDropTarget': 'dpg.mvThemeCol_DragDropTarget',
    'FrameBg': 'dpg.mvThemeCol_FrameBg',
    'FrameBgActive': 'dpg.mvThemeCol_FrameBgActive',
    'FrameBgHovered': 'dpg.mvThemeCol_FrameBgHovered',
    'Header': 'dpg.mvThemeCol_Header',
    'HeaderActive': 'dpg.mvThemeCol_HeaderActive',
    'HeaderHovered': 'dpg.mvThemeCol_HeaderHovered',
    'MenuBarBg': 'dpg.mvThemeCol_MenuBarBg',
    'ModalWindowDimBg': 'dpg.mvThemeCol_ModalWindowDimBg',
    'NavHighlight': 'dpg.mvThemeCol_NavHighlight',
    'NavWindowingDimBg': 'dpg.mvThemeCol_NavWindowingDimBg',
    'NavWindowingHighlight': 'dpg.mvThemeCol_NavWindowingHighlight',
    'PlotHistogram': 'dpg.mvThemeCol_PlotHistogram',
    'PlotHistogramHovered': 'dpg.mvThemeCol_PlotHistogramHovered',
    'PlotLines': 'dpg.mvThemeCol_PlotLines',
    'PlotLinesHovered': 'dpg.mvThemeCol_PlotLinesHovered',
    'PopupBg': 'dpg.mvThemeCol_PopupBg',
    'ResizeGrip': 'dpg.mvThemeCol_ResizeGrip',
    'ResizeGripActive': 'dpg.mvThemeCol_ResizeGripActive',
    'ResizeGripHovered': 'dpg.mvThemeCol_ResizeGripHovered',
    'ScrollbarBg': 'dpg.mvThemeCol_ScrollbarBg',
    'ScrollbarGrab': 'dpg.mvThemeCol_ScrollbarGrab',
    'ScrollbarGrabActive': 'dpg.mvThemeCol_ScrollbarGrabActive',
    'ScrollbarGrabHovered': 'dpg.mvThemeCol_ScrollbarGrabHovered',
    'Separator': 'dpg.mvThemeCol_Separator',
    'SeparatorActive': 'dpg.mvThemeCol_SeparatorActive',
    'SeparatorHovered': 'dpg.mvThemeCol_SeparatorHovered',
    'SliderGrab': 'dpg.mvThemeCol_SliderGrab',
    'SliderGrabActive': 'dpg.mvThemeCol_SliderGrabActive',
    'Tab': 'dpg.mvThemeCol_Tab',
    'TabActive': 'dpg.mvThemeCol_TabActive',
    'TabHovered': 'dpg.mvThemeCol_TabHovered',
    'TabUnfocused': 'dpg.mvThemeCol_TabUnfocused',
    'TabUnfocusedActive': 'dpg.mvThemeCol_TabUnfocusedActive',
    'TableBorderLight': 'dpg.mvThemeCol_TableBorderLight',
    'TableBorderStrong': 'dpg.mvThemeCol_TableBorderStrong',
    'TableHeaderBg': 'dpg.mvThemeCol_TableHeaderBg',
    'TableRowBg': 'dpg.mvThemeCol_TableRowBg',
    'TableRowBgAlt': 'dpg.mvThemeCol_TableRowBgAlt',
    'Text': 'dpg.mvThemeCol_Text',
    'TextDisabled': 'dpg.mvThemeCol_TextDisabled',
    'TextSelectedBg': 'dpg.mvThemeCol_TextSelectedBg',
    'TitleBg': 'dpg.mvThemeCol_TitleBg',
    'TitleBgActive': 'dpg.mvThemeCol_TitleBgActive',
    'TitleBgCollapsed': 'dpg.mvThemeCol_TitleBgCollapsed',
    'WindowBg': 'dpg.mvThemeCol_WindowBg',
    'ChildBg': 'dpg.mvThemeCol_ChildBg',

}

ignore: list[str] = [
    'disabledAlpha',
    'windowMenuButtonPosition',
    'columnsMinSpacing',
    'tabBorderSize',
    'tabMinWidthForCloseButton',
    'colorButtonPosition',
    'colors',
]

replace_themes: list[list[str, str]] = [
    # THEME --copy value to-> THEME
    ['WindowBg', 'ChildBg'],
    ['WindowBg', 'PopupBg'],
]

with open("themes.toml", "rb") as f:
    data = tomllib.load(f)['themes']
    for theme in data:
        name: str = theme['name']
        styles: dict = theme['style']
        colors: dict = styles['colors']
        for replace_theme in replace_themes:
            if replace_theme[1] in styles:
                styles[replace_theme[1]] = styles[replace_theme[0]]
            if replace_theme[1] in colors:
                colors[replace_theme[1]] = colors[replace_theme[0]]

        output_string = f"# Author: {theme['author']}\n" \
                        "from __future__ import annotations\n\n" \
                        "from typing import Optional, Sequence\n\n" \
                        "import dearpygui.dearpygui as dpg\n\n" \
                        f'name = """{name}"""\n' \
                        "styles: dict[int, Sequence[float]] = {\n"
        # styles
        for style_name in list(styles.keys()):
            if style_name in ignore:
                continue
            style_value = f"[{str(styles[style_name]).replace('[', '').replace(']', '')}]"
            style_name = rename.get(style_name, None)
            if style_name is None:
                raise ValueError(f"Unknown theme type: {style_name}")
            output_string += f"    {style_name}: {style_value},\n"
        output_string += '}\n'
        # pprint(colors)

        # colors
        output_string += 'colors: dict[int, Sequence[int, int, int, Optional[int]]] = {\n'
        for color_name in list(colors.keys()):
            if color_name in ignore:
                continue
            color_value = list(eval(colors[color_name].replace('rgb', '').replace('a', '')))
            color_value[-1] = int(color_value[-1] * 255)
            color_name = rename.get(color_name, None)
            if color_name is None:
                raise ValueError(f"Unknown color type: {color_name}")
            output_string += f"    {color_name}: {color_value},\n"
        output_string += '}\n'

        file_name = name.lower().replace(' ', '_')
        file_name = list(filter(lambda char: char in string.ascii_lowercase + "_", file_name))
        file_name = ''.join(file_name)
        with open(os.path.join('themes', file_name + ".py"), "w") as file:
            file.write(output_string)

        # TODO: auto generate __init__.py
        # print(f"{file_name.upper()} = {file_name}")
        # print(f"from . import {file_name}")
