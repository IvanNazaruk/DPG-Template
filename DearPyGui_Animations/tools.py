def math_round(number: float) -> int:
    return int(number + (0.5 if number > 0 else -0.5))
