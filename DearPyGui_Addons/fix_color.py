from typing import Sequence


def fix_color(color: Sequence[int]) -> Sequence[int]:
    color = list(color[:4:])
    for _ in range(4 - len(color)):
        color.append(255)
    return color


def fix_float_color(color: Sequence[float]) -> Sequence[int]:
    color = list(color[:4:])
    for i in range(len(color)):
        color = int(color[i] * 255)
    for _ in range(4 - len(color)):
        color.append(255)
    return color
