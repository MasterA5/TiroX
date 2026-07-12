from flet import (
    AlertDialog,
    Colors,
    Column,
    Control,
    FontWeight,
    Icon,
    Icons,
    Image,
    Row,
    Text,
)

from components.StylishButton import StylishButton


class StylishDialog(AlertDialog):
    def __init__(
        self,
        title: Control | str | None = None,
        content: Control | None = None,
        actions: list[Control] | None = None,
    ):
        super().__init__()
        self.title = title if isinstance(title, Control) else Text(title)
        self.content = Column(controls=[content], tight=True)
        self.actions = (
            [
                StylishButton(
                    text="Cerrar",
                    icon=Icons.CLOSE,
                    on_click=lambda e: self.page.close(e.control.parent),
                )
            ]
            if not actions
            else actions
        )


class QRSuccessfullyCreated(StylishDialog):
    def __init__(self, image_src: str):
        super().__init__(
            title=Row(
                controls=[
                    Icon(Icons.QR_CODE, color=Colors.DEEP_PURPLE_ACCENT_200),
                    Text(
                        "Codigo QR Generado!!",
                        color=Colors.DEEP_PURPLE_ACCENT_200,
                        weight=FontWeight.BOLD,
                    ),
                ]
            ),
            content=Image(
                src_base64=image_src,
            ),
        )


class FieldsError(StylishDialog):
    def __init__(self):
        super().__init__(
            title=Row(
                controls=[
                    Icon(Icons.ERROR, color=Colors.DEEP_PURPLE_ACCENT_200, size=30),
                    Text(
                        "Error",
                        color=Colors.DEEP_PURPLE_ACCENT_200,
                        weight=FontWeight.BOLD,
                    ),
                ],
            ),
            content=Text("Por favor, completa todos los campos"),
        )


class QRProccessError(StylishDialog):
    def __init__(
        self,
    ):
        super().__init__(
            title=Text("Error"),
            content=Column(
                controls=[
                    Text("Error al procesar el código QR"),
                    Text("Porfavor Vuelve a Escanearlo De Nuevo"),
                ]
            ),
        )
