import dearpygui.dearpygui as dpg
from dearpygui import demo

from DPG_modules import Theme as dpg_theme
from DPG_modules.Addons import CheckBoxSlider
from DPG_modules.Addons.title_bar import set_dark_mode
from DPG_modules.ImageController import add_image
from Resources.textures import ChaineDisabled, ChaineEnabled


class MainWindow:
    window: int = None

    def __init__(self):
        with dpg.window() as self.window:
            dpg.add_text("Demo: work-in-progress")
            dpg.add_button(label="Open DPG demo", callback=demo.show_demo)
            CheckBoxSlider(callback=lambda flag: set_dark_mode(flag)).create()
            dpg_theme.add_theme_picker()
            add_image(ChaineDisabled.get())
            add_image(ChaineEnabled.get())

    def test_callback(self, *args, **kwargs):
        print('hello:', args, kwargs)
