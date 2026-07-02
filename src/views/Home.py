from flet import (
    AppBar,
    BoxShadow,
    Colors,
    Column,
    Container,
    ControlEvent,
    FontWeight,
    IconButton,
    Icons,
    MainAxisAlignment,
    NavigationBar,
    NavigationBarDestination,
    NavigationDrawer,
    NavigationDrawerDestination,
    Offset,
    Row,
    SafeArea,
    ShadowBlurStyle,
    Slider,
    Text,
    TextSpan,
    TextStyle,
    View,
    margin,
    padding,
)
from flet_routing import FletRouter, Params

from components.AnimatedButton import AnimatedButton
from components.Chart import TiroXChart
from components.LastResultCard import LastResultCard


class HomeView(View):
    def __init__(self, params: Params):
        super().__init__()
        self.route = "/"
        self.params = params
        self.router: FletRouter = self.params.router
        self.appbar = AppBar(
            title=Text(
                "Tiro",
                size=30,
                weight=FontWeight.BOLD,
                spans=[
                    TextSpan(
                        "X",
                        style=TextStyle(color=Colors.DEEP_PURPLE_ACCENT_200),
                    )
                ],
            ),
            center_title=True,
            actions=[
                IconButton(
                    icon=Icons.NOTIFICATIONS_OUTLINED,
                ),
            ],
        )
        self.drawer = NavigationDrawer(
            controls=[
                NavigationDrawerDestination(label="Home", icon=Icons.HOME),
                NavigationDrawerDestination(label="Your Data", icon=Icons.FINGERPRINT),
                NavigationDrawerDestination(label="Settings", icon=Icons.SETTINGS),
            ],
            on_change=self.__handle_nav
        )
        self.navigation_bar = NavigationBar(
            destinations=[
                NavigationBarDestination(label="Home", icon=Icons.HOME),
                NavigationBarDestination(label="Your Data", icon=Icons.FINGERPRINT),
                NavigationBarDestination(label="Settings", icon=Icons.SETTINGS),
            ],
            on_change=self.__handle_nav
        )
        self.main_container = SafeArea(content=self.__build_home_content(), expand=True)
        self.controls = [self.main_container]
        self.scroll = "auto"
        self.expand = True

    def __build_home_content(self):
        return Column(
            controls=[
                Container(
                    content=Text("Resumen", weight=FontWeight.BOLD, size=16),
                    padding=padding.only(top=30),
                ),
                LastResultCard(),
                Container(
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Text(
                                        "En rango normal",
                                        weight=FontWeight.BOLD,
                                        size=16,
                                    ),
                                    IconButton(
                                        icon=Icons.INFO_OUTLINE,
                                        icon_color=Colors.GREY_400,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            Container(height=3),
                            Column(
                                controls=[
                                    Text(
                                        "Rango de referencia",
                                        weight=FontWeight.W_500,
                                    ),
                                    Text(
                                        "0.27 - 4.20 mUI/L",
                                        weight=FontWeight.W_400,
                                    ),
                                ],
                                spacing=3,
                            ),
                            Container(height=3),
                            Slider(),
                        ]
                    ),
                    padding=15,
                    border_radius=20,
                    shadow=BoxShadow(
                        blur_radius=1.4,
                        spread_radius=1.3,
                        color=Colors.GREY_300,
                    ),
                    bgcolor=Colors.WHITE,
                ),
                TiroXChart(),
                Row(
                    controls=[
                        AnimatedButton(
                            on_click=lambda e: self.router.push(
                                path="/create/register"
                            ),
                            icon=Icons.ADD,
                            text="Nuevo Registro"
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
            ]
        )

    def __build_history_content(self):
        return Column(
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    Text("TSH", size=19, weight=FontWeight.W_500),
                                    Text(
                                        "2.18",
                                        color=Colors.GREEN,
                                        size=20,
                                        weight=FontWeight.BOLD,
                                        spans=[
                                            TextSpan(
                                                " mUI/L",
                                                style=TextStyle(
                                                    color=Colors.GREEN, size=10
                                                ),
                                            )
                                        ],
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            Row(
                                controls=[
                                    Text("20 may 2024"),
                                    Container(
                                        content=Text(
                                            "Normal",
                                            color=Colors.GREEN,
                                            weight=FontWeight.BOLD,
                                        ),
                                        padding=padding.only(
                                            left=10, right=10, top=3, bottom=3
                                        ),
                                        bgcolor=Colors.LIGHT_GREEN_100,
                                        border_radius=20,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ]
                    ),
                    padding=20,
                    border_radius=20,
                    shadow=BoxShadow(
                        spread_radius=1.12,
                        blur_radius=1.12,
                        blur_style=ShadowBlurStyle.OUTER,
                    ),
                    bgcolor=Colors.WHITE,
                    margin=margin.all(10),
                )
                for i in range(3)
            ]
        )

    def __handle_nav(self, e: ControlEvent):
        idx = int(e.data)

        match idx:
            case 0:
                self.main_container.content = self.__build_home_content()
            case 1:
                self.main_container.content = self.__build_history_content()
            case 2:
                self.main_container.content = Text("This Page Still in development")

        self.main_container.update()
        self.page.update()
