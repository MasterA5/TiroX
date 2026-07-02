from flet import (
    AppBar,
    Colors,
    Column,
    Container,
    Dropdown,
    DropdownOption,
    FontWeight,
    Icon,
    IconButton,
    Icons,
    InputBorder,
    MainAxisAlignment,
    PagePlatform,
    Row,
    Text,
    TextField,
    View,
    border,
    padding,
)
from flet_routing import FletRouter, Params

from components.AnimatedButton import AnimatedButton


class NewRegisterView(View):
    def __init__(self, params: Params):
        super().__init__("/create/register")
        self.params = params
        self.router: FletRouter = self.params.router
        self.scroll = "auto"
        self.controls = [
            Column(
                controls=[
                    Row(
                        controls=[
                            Container(
                                content=Icon(
                                    Icons.SCIENCE, size=60, color=Colors.WHITE
                                ),
                                padding=10,
                                bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                                border_radius=200,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Row(
                        controls=[
                            Container(
                                content=Text(
                                    "Crea Un Nuevo Registro",
                                    size=16,
                                    weight=FontWeight.W_700,
                                ),
                                padding=padding.only(top=20),
                            )
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Container(
                        content=Column(
                            controls=[
                                Text("Selecciona La Hormona"),
                                Dropdown(
                                    options=[
                                        DropdownOption(
                                            key="TSH", content=Text("Hormona TSH")
                                        )
                                    ],
                                    value="TSH",
                                    expand=True,
                                ),
                                Container(
                                    content=Column(
                                        controls=[
                                            Text("Resultado"),
                                            TextField(label="Resultado"),
                                        ]
                                    ),
                                    padding=padding.only(top=20),
                                ),
                                Container(
                                    content=Column(
                                        controls=[
                                            Text("Fecha De Analisis"),
                                            Dropdown(
                                                label="Fecha De Analisis", expand=True
                                            ),
                                        ]
                                    ),
                                    padding=padding.only(top=20),
                                ),
                                Container(
                                    content=Column(
                                        controls=[
                                            Text("Notas"),
                                            Container(
                                                content=TextField(
                                                    label="Notas",
                                                    multiline=True,
                                                    expand=True,
                                                    border=InputBorder.NONE,
                                                ),
                                                height=200,
                                                border=border.all(2, Colors.GREY_300),
                                                border_radius=20,
                                                padding=10,
                                            ),
                                            Row(
                                                controls=[
                                                    AnimatedButton(
                                                        text="Guardar",
                                                        final_width=110,
                                                        icon=Icons.SAVE_ALT,
                                                    ),
                                                ],
                                                alignment=MainAxisAlignment.CENTER,
                                            ),
                                        ]
                                    ),
                                    padding=padding.only(top=20)
                                ),
                            ]
                        )
                    ),
                ]
            )
        ]
        self.appbar = AppBar(
            title=Text("Nuevo Registro", size=16, weight=FontWeight.W_700),
            leading=IconButton(
                Icons.ARROW_BACK
                if self.router.page.platform != PagePlatform.IOS
                else Icons.ARROW_BACK_IOS,
                on_click=lambda e: self.router.back(),
            ),
            center_title=True,
        )
