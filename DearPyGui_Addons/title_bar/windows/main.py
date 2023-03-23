import sys

import win32mica

from .tools import get_hwnd, removeBackground


def set_dark_mode(flag: bool):
    hwnd: int = get_hwnd()
    if hwnd is None:
        return
    if sys.getwindowsversion().build >= 22000:
        removeBackground()

    win32mica.ApplyMica(hwnd, flag)
