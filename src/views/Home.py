import random
import uuid

from flet import (
    AppBar,
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
    Row,
    SafeArea,
    Text,
    TextSpan,
    TextStyle,
    View,
    padding,
)
from flet_routing import FletRouter, Params

from components.AnimatedButton import AnimatedButton
from components.Chart import TiroXChart
from components.HistoryCard import HistoryCard
from components.LastResultCard import LastResultCard
from components.RangeCard import RangeCard


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
            on_change=self.__handle_nav,
        )
        self.navigation_bar = NavigationBar(
            destinations=[
                NavigationBarDestination(label="Home", icon=Icons.HOME),
                NavigationBarDestination(label="Your Data", icon=Icons.FINGERPRINT),
                NavigationBarDestination(label="Settings", icon=Icons.SETTINGS),
            ],
            on_change=self.__handle_nav,
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
                RangeCard(),
                TiroXChart(),
                Row(
                    controls=[
                        AnimatedButton(
                            on_click=lambda e: self.router.push(
                                path="/create/register"
                            ),
                            icon=Icons.ADD,
                            text="Nuevo Registro",
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
            ]
        )

    def __build_history_content(self):
        return Column(
            controls=[
                HistoryCard(
                    on_click=lambda e: self.router.push(
                        f"/detail/{uuid.uuid4()}"
                    ),
                    value=float(f"{random.uniform(1, 9):.2f}"),
                    date="20 may 2024",
                ),
            ]
        )

    def __handle_nav(self, e: ControlEvent):
        if not e:
            return

        idx = int(e.data)

        match idx:
            case 0:
                self.main_container.content = self.__build_home_content()
            case 1:
                self.main_container.content = self.__build_history_content()
            case 2:
                self.main_container.content = Text("This Page Still in development")

        self.navigation_bar.selected_index = idx
        self.drawer.selected_index = idx

        self.main_container.update()
        self.page.update()
