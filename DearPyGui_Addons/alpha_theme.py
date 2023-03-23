import dearpygui.dearpygui as dpg

alpha_themes: dict[int, int] = {}


def get_alpha_theme(value: float) -> int:
    value = int(value * 1000)
    theme = alpha_themes.get(value, None)
    if theme is not None:
        return theme
    with dpg.theme() as theme:
        with dpg.theme_component(parent=theme) as theme_component:
            dpg.add_theme_style(dpg.mvStyleVar_Alpha, value / 1000, parent=theme_component)
    alpha_themes[value] = theme
    return theme
