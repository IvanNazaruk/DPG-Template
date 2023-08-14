from Resources import fonts


def get_loading_indicator_radius(width: int, height: int) -> float:
    return min(width, height) / fonts.font_size
