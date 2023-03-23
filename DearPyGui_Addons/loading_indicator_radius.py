import fonts


def get_loading_indicator_radius(width: int, height: int) -> float:
    radius = width if width < height else height
    radius = radius / fonts.font_size
    return radius
