from flet import Colors


def get_color_by_value(
    value: float | int | str,
    bg_custom_colors: list[Colors] | None = [
        Colors.LIGHT_GREEN_100,
        Colors.with_opacity(0.4, Colors.AMBER_200),
        Colors.with_opacity(0.4, Colors.RED),
    ],
    txt_custom_colors: list[Colors] | None = [
        Colors.GREEN_300,
        Colors.YELLOW_800,
        Colors.RED_800,
    ],
):
    bg_low_color, bg_normal_color, bg_high_color = bg_custom_colors
    txt_low_color, txt_normal_color, txt_high_color = txt_custom_colors

    bgcolor: Colors = bg_low_color
    text_color: Colors = txt_low_color

    if value > 0 and value < 4:
        bgcolor = bg_low_color
        text_color = txt_low_color
    elif value > 4 and value <= 6:
        bgcolor = bg_normal_color
        text_color: Colors = txt_normal_color
    elif value > 6:
        bgcolor = bg_high_color
        text_color: Colors = txt_high_color
    else:
        return None, None

    return bgcolor, text_color
