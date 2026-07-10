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
    KeyboardType,
    MainAxisAlignment,
    PagePlatform,
    Row,
    SnackBar,
    SnackBarBehavior,
    Text,
    TextField,
    View,
    border,
    padding,
)
from flet_routing import FletRouter, Params

from components.AnimatedButton import AnimatedButton
from core.RegisterManager import Register, RegisterManager


class NewRegisterView(View):
    def __init__(self, params: Params, register_manager: RegisterManager | None = None):
        super().__init__("/create/register")
        self.params = params
        self.router: FletRouter = self.params.router
        self.register_manager = register_manager
        self.scroll = "auto"
        self.hormone_field = Dropdown(
            options=[DropdownOption(key="TSH", content=Text("Hormona TSH"))],
            label="Selecciona el tipo de hormona",
            expand=True,
        )
        self.result_field = TextField(
            label="Resultado", keyboard_type=KeyboardType.NUMBER
        )
        self.notes_field = TextField(
            label="Notas",
            multiline=True,
            expand=True,
            border=InputBorder.NONE,
        )
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
                                self.hormone_field,
                                Container(
                                    content=Column(
                                        controls=[
                                            Text("Resultado"),
                                            self.result_field,
                                        ]
                                    ),
                                    padding=padding.only(top=20),
                                ),
                                Container(
                                    content=Column(
                                        controls=[
                                            Text("Notas"),
                                            Container(
                                                content=self.notes_field,
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
                                                        on_click=self.handle_sumbit,
                                                    ),
                                                ],
                                                alignment=MainAxisAlignment.CENTER,
                                            ),
                                        ]
                                    ),
                                    padding=padding.only(top=20),
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

    def handle_sumbit(self, e):
        if not self.hormone_field.value:
            return

        if not self.result_field.value:
            return

        register = self.register_manager.add_register(
            Register(
                hormone=self.hormone_field.value,
                value=float(self.result_field.value),
                notes=self.notes_field.value,
            )
        )

        self.page.open(
            SnackBar(
                content=Row(
                    controls=[
                        Icon(Icons.CHECK_CIRCLE, color=Colors.WHITE),
                        Text("Registro Creado"),
                    ]
                ),
                behavior=SnackBarBehavior.FLOATING,
                bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
            )
        )

        if register:
            self.router.replace("/")
