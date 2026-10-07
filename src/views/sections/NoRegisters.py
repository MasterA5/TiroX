from flet import (
    Colors,
    Column,
    Container,
    FontWeight,
    Icon,
    Icons,
    MainAxisAlignment,
    OptionalControlEventCallable,
    Row,
    Text,
    alignment,
)

from components.StylishButton import StylishButton


class NoRegistersSection(Container):
    def __init__(self, on_create_first_register: OptionalControlEventCallable = None):
        super().__init__()
        self.expand = True
        self.on_create_first_register = on_create_first_register
        self.alignment = alignment.center
        self.content = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment="center",
            controls=[
                Container(
                    width=80,
                    height=80,
                    bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                    border_radius=40,
                    alignment=alignment.center,
                    content=Icon(
                        Icons.HISTORY,
                        size=42,
                        color=Colors.WHITE,
                    ),
                ),
                Text(
                    "Todavía no tienes registros",
                    size=22,
                    weight=FontWeight.BOLD,
                ),
                Column(
                    controls=[
                        Text(
                            value="Los resultados aparecerán aquí",
                            size=15,
                            color=Colors.GREY_500,
                            text_align="center",
                        ),
                        Text(
                            value=" cuando agregues uno nuevo.",
                            size=15,
                            color=Colors.GREY_500,
                            text_align="center",
                        ),
                    ],
                    spacing=0,
                ),
                Row(
                    controls=[
                        StylishButton(
                            text="Crea Tu Primer Registro",
                            icon=Icons.ADD,
                            on_click=self.on_create_first_register,
                        ),
                    ],
                    width=230,
                ),
            ],
        )
