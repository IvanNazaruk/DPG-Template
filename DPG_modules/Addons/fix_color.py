from typing import Sequence


def fix_color(color: Sequence[int]) -> Sequence[int]:
    color = list(map(int, color[:4:]))
    color.extend([255] * (4 - len(color)))
    return color


def fix_float_color(color: Sequence[float]) -> Sequence[int]:
    color = list(color[:4:])
    for i in range(len(color)):
        color = int(color[i] * 255)
    color.extend([255] * (4 - len(color)))
    return color
