from flet import Icons


def get_icon_by_value(value: float | int | str, icons: list[Icons] | None = None):
    if not icons:
        icons = [
            Icons.ARROW_DOWNWARD_OUTLINED,
            Icons.WARNING_AMBER_OUTLINED,
            Icons.ARROW_UPWARD_OUTLINED,
        ]

    if value > 0 and value < 4:
        return icons[0]
    elif value > 4 and value <= 6:
        return icons[1]
    elif value > 6:
        return icons[2]
    else:
        return Icons.ERROR
