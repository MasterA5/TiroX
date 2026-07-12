from flet import (
    Colors,
    ColorValue,
    Control,
    Icon,
    Icons,
    IconValue,
    Row,
    SnackBar,
    SnackBarBehavior,
    Text,
)


class StylishSnackBar(SnackBar):
    def __init__(
        self,
        text: Text | str,
        icon: IconValue | None = None,
        bgcolor: ColorValue = Colors.DEEP_PURPLE_ACCENT_200,
    ):
        super().__init__(None)
        self.text = text if isinstance(text, Control) else Text(text)
        self.icon = icon
        self.content = Row(
            controls=[
                Icon(
                    name=icon,
                    color=Colors.WHITE,
                    visible=self.icon is not None,
                ),
                self.text,
            ]
        )
        self.behavior = SnackBarBehavior.FLOATING
        self.bgcolor = bgcolor


class RegisterCreatedSuccefull(StylishSnackBar):
    def __init__(self):
        super().__init__(text="Registro Creado", icon=Icons.CHECK_CIRCLE)


class RegisterDeletedSuccefull(StylishSnackBar):
    def __init__(self):
        super().__init__(text="Registro Eliminado", icon=Icons.CHECK_CIRCLE)
