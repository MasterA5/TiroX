from flet import Icons


def get_icon_by_value(value: float | int | str):
    if value < 4:
        return Icons.ARROW_DOWNWARD_OUTLINED
    elif value > 4 and value < 6:
        return Icons.WARNING_AMBER_OUTLINED
    elif value > 6:
        return Icons.ARROW_UPWARD_OUTLINED
    else:
        return None
