from __future__ import annotations

from typing import Sequence

import dearpygui.dearpygui as dpg


def get_text_size(text: str, *, wrap_width: float = -1.0, font: int | str = 0, **kwargs) -> Sequence[int, int]:
    strip_text = text.strip()
    while 1:
        size: list[float, float] = dpg.get_text_size(text, wrap_width=wrap_width, font=font, **kwargs)

        if size is None:
            continue
        elif size[1] == 0:
            continue
        elif size[0] == 0 and strip_text != "":
            continue
        break
    return [int(size[0]), int(size[1])]
