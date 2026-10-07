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
        self.text = (
            text if isinstance(text, Control) else Text(text, color=Colors.WHITE)
        )
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


class SyncSuccefull(StylishSnackBar):
    def __init__(self):
        super().__init__(
            text="Registros Sincronizados", icon=Icons.CLOUD_DONE_OUTLINED
        )


class SyncFailed(StylishSnackBar):
    def __init__(self):
        super().__init__(
            text="No Se Pudo Sincronizar Con El Servidor",
            icon=Icons.CLOUD_OFF_OUTLINED,
            bgcolor=Colors.RED_400,
        )


class ErrorSnackBar(StylishSnackBar):
    def __init__(self, message: str):
        super().__init__(text=message, icon=Icons.ERROR_OUTLINE, bgcolor=Colors.RED_400)
