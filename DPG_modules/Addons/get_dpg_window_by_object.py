import dearpygui.dearpygui as dpg


def get_dpg_window_by_object(dpg_item: int | str) -> int | str:
    while True:
        if not dpg.does_item_exist(dpg_item):
            return 0
        if dpg.get_item_info(dpg_item)['type'] == 'mvAppItemType::mvWindowAppItem':
            return dpg_item
        dpg_item = dpg.get_item_parent(dpg_item)
