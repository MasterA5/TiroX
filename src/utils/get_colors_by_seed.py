from flet import Colors


def get_colors_by_seed(seed: str):
    return [Colors(color.value) for color in list(Colors) if "purple" in color.value]
