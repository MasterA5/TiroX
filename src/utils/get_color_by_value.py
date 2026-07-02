from flet import Colors


def get_color_by_value(value: float | int | str):
    tag_text = ""
    bgcolor: Colors = Colors.LIGHT_GREEN_100
    text_color: Colors = Colors.GREEN_300

    if value < 4:
        tag_text = "Normal"
    elif value > 4 and value < 6:
        tag_text = "Limite Alto"
        bgcolor = Colors.with_opacity(0.4, Colors.AMBER_200)
        text_color: Colors = Colors.YELLOW_800
    elif value > 6:
        tag_text = "Alto"
        bgcolor = Colors.with_opacity(0.4, Colors.RED)
        text_color: Colors = Colors.RED_800
    else:
        return None, None, None

    return tag_text, bgcolor, text_color
