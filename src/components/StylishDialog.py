from flet import (
    AlertDialog,
    Colors,
    Column,
    Container,
    Control,
    FontWeight,
    Icon,
    Icons,
    Image,
    OptionalControlEventCallable,
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
        super().__init__(modal=True)

        # Título
        if title is None:
            self.title = None
        elif isinstance(title, Control):
            self.title = title
        else:
            self.title = Text(title)

        # Contenido
        if content is None:
            self.content = None
        elif isinstance(content, Column):
            self.content = content
        else:
            self.content = Column(
                controls=[content],
                tight=True,
            )

        # Acciones
        self.actions = actions or [
            StylishButton(
                text="Cerrar",
                icon=Icons.CLOSE,
                on_click=lambda e: self.page.close(self),
            )
        ]


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
    def __init__(self):
        super().__init__(
            title=Text("Error"),
            content=Column(
                controls=[
                    Text("Error al procesar el código QR"),
                    Text("Porfavor Vuelve a Escanearlo De Nuevo"),
                ]
            ),
        )

class QRGenerationError(StylishDialog):
    def __init__(self, error: str):
        super().__init__(
            title=Text("Error"),
            content=Column(
                controls=[
                    Text("Error Al Generar El Código QR"),
                    Text("Porfavor Vuelve a Intentarlo De Nuevo"),
                    Text(error),
                ]
            ),
        )


class DeleteRegisterConfirm(StylishDialog):
    def __init__(self, on_delete: OptionalControlEventCallable = None):
        super().__init__()
        self.title = Text("Estas Seguro Que Quieres Eliminar Este Registro?")
        self.actions = [
            StylishButton(text="Eliminar", icon=Icons.DELETE, on_click=on_delete),
            Container(height=10),
            StylishButton(
                text="Cancelar",
                icon=Icons.CANCEL,
                on_click=lambda e: self.page.close(e.control.parent),
            ),
        ]
