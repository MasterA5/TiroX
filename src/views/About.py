from flet import (
    AppBar,
    Colors,
    Column,
    Container,
    CrossAxisAlignment,
    FontWeight,
    Icon,
    Icons,
    LinearGradient,
    MainAxisAlignment,
    Row,
    SafeArea,
    ScrollMode,
    Text,
    TextAlign,
    View,
    alignment,
    padding,
)
from flet_routing import Params


class InfoCard(Container):
    def __init__(
        self,
        icon: str,
        title: str,
        description: str,
        icon_color: str = Colors.DEEP_PURPLE_ACCENT_200,
    ):
        super().__init__()
        self.border_radius = 18
        self.bgcolor = Colors.SURFACE_CONTAINER_HIGHEST
        self.padding = 20
        self.content = Row(
            spacing=15,
            vertical_alignment=CrossAxisAlignment.START,
            controls=[
                Icon(
                    icon,
                    size=34,
                    color=icon_color,
                ),
                Column(
                    expand=True,
                    spacing=4,
                    controls=[
                        Text(
                            title,
                            weight=FontWeight.BOLD,
                            size=18,
                        ),
                        Text(
                            description,
                            color=Colors.GREY_500,
                            size=14,
                        ),
                    ],
                ),
            ],
        )


class VersionCard(Container):
    def __init__(self, version: str):
        super().__init__()
        self.border_radius = 20
        self.padding = 25
        self.gradient = LinearGradient(
            colors=[
                Colors.DEEP_PURPLE_400,
                Colors.DEEP_PURPLE_ACCENT_200,
            ]
        )
        self.content = Row(
            controls=[
                Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Icon(
                            Icons.SCIENCE,
                            size=60,
                            color=Colors.WHITE,
                        ),
                        Text(
                            "TiroX",
                            size=30,
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        Text(
                            f"Versión {version}",
                            color=Colors.WHITE70,
                        ),
                    ],
                ),
            ],
            expand=True,
            alignment=MainAxisAlignment.CENTER,
        )
        self.expand = True


class AboutView(View):
    def __init__(self, params: Params):
        super().__init__("/about")

        self.appbar = AppBar(
            title=Text("Acerca de"),
            center_title=True,
        )

        self.scroll = ScrollMode.AUTO

        self.controls = [
            SafeArea(
                expand=True,
                content=Column(
                    scroll=ScrollMode.AUTO,
                    spacing=22,
                    controls=[
                        Column(
                            spacing=4,
                            controls=[
                                Text(
                                    "Acerca de TiroX",
                                    size=30,
                                    weight=FontWeight.BOLD,
                                ),
                                Text(
                                    "Conoce un poco más sobre el proyecto.",
                                    color=Colors.GREY_500,
                                    size=15,
                                ),
                            ],
                        ),
                        VersionCard("1.0.0"),
                        InfoCard(
                            Icons.GROUP_OUTLINED,
                            "Nuestro Equipo",
                            "TiroX fue desarrollado por un equipo de estudiantes "
                            "seleccionados para participar en un programa de "
                            "mentorías, donde aplicaron sus conocimientos para "
                            "crear una herramienta útil y moderna.",
                        ),
                        InfoCard(
                            Icons.MONITOR_HEART_OUTLINED,
                            "Objetivo",
                            "Facilitar el seguimiento y la visualización de "
                            "resultados médicos mediante una aplicación intuitiva, "
                            "rápida y agradable de utilizar.",
                        ),
                        InfoCard(
                            Icons.CODE,
                            "Tecnologías",
                            "Python • Flet • Flutter • Material Design 3",
                        ),
                        Container(
                            alignment=alignment.center,
                            padding=padding.only(top=10, bottom=20),
                            content=Text(
                                "© 2026 TiroX\nTodos los derechos reservados.",
                                text_align=TextAlign.CENTER,
                                color=Colors.GREY_500,
                                size=13,
                            ),
                        ),
                        Container(
                            alignment=alignment.center,
                            padding=padding.only(top=10, bottom=20),
                            content=Text(
                                "Esta aplicacion es unicamente para\n" \
                                "propositos de muestra y ejemplificacion.",
                                text_align=TextAlign.CENTER,
                                color=Colors.GREY_500,
                                size=13,
                            ),
                        ),
                    ],
                ),
            )
        ]
