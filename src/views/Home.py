from uuid import UUID

from flet import (
    AppBar,
    Colors,
    Column,
    Container,
    ControlEvent,
    CupertinoContextMenu,
    CupertinoContextMenuAction,
    FontWeight,
    Icon,
    IconButton,
    Icons,
    MainAxisAlignment,
    NavigationBar,
    NavigationBarDestination,
    NavigationBarLabelBehavior,
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
from components.HistoryCard import HistoryCard
from components.LastResultCard import LastResultCard
from components.RangeCard import RangeCard
from core.RegisterManager import RegisterManager


class HomeView(View):
    def __init__(self, params: Params, manager: RegisterManager | None = None):
        super().__init__()
        self.route = "/"
        self.params = params
        self.router: FletRouter = self.params.router
        self.register_manager = manager
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
                Container(
                    content=Text(
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
                    padding=padding.only(left=10),
                ),
                NavigationDrawerDestination(label="Home", icon=Icons.HOME),
                NavigationDrawerDestination(label="Your Data", icon=Icons.FINGERPRINT),
                NavigationDrawerDestination(label="Settings", icon=Icons.SETTINGS),
            ],
            on_change=self.__handle_nav,
            tile_padding=23,
        )
        self.navigation_bar = NavigationBar(
            destinations=[
                NavigationBarDestination(label="Home", icon=Icons.HOME),
                NavigationBarDestination(label="Your Data", icon=Icons.FINGERPRINT),
                NavigationBarDestination(label="Settings", icon=Icons.SETTINGS),
            ],
            on_change=self.__handle_nav,
            label_behavior=NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        )
        self.main_container = SafeArea(content=self.__build_home_content(), expand=True)
        self.controls = [self.main_container]
        self.scroll = "auto"
        self.expand = True
        self.current_index = 0
        self.history_page = Column(controls=[], expand=True, scroll="auto")

    def __build_home_content(self):
        last_register = self.register_manager.get_last_register()

        if not last_register:
            last_result_card = Container(
                content=Row(
                    controls=[
                        Icon(Icons.ERROR_OUTLINE, color=Colors.PURPLE_200, size=30),
                        Text("No Se econtraron registros", color=Colors.WHITE, size=25),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                padding=15,
                bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                border_radius=20,
                height=200,
            )
        else:
            last_result_card = LastResultCard(
                hormone=last_register.hormone,
                value=last_register.value,
                date=last_register.date,
            )

        return Column(
            controls=[
                Container(
                    content=Text("Resumen", weight=FontWeight.BOLD, size=16),
                    padding=padding.only(top=5),
                ),
                last_result_card,
                RangeCard(last_register.value),
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
        self.history_page.controls.clear()
        registers = self.register_manager.get_all_registers()

        if not registers:
            self.history_page.controls.append(
                Row(
                    controls=[
                        Column(
                            controls=[Text("No se encontraron registros", size=30)],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                )
            )

        for register in registers:
            reg_id = register.id
            reg_value = register.value
            reg_date = register.date

            card = CupertinoContextMenu(
                content=Container(
                    content=HistoryCard(
                        on_click=lambda e, id=reg_id: self.router.push(
                            f"/detail/{id}", {"lst_idx": 1}
                        ),
                        value=float(reg_value),
                        date=reg_date,
                    ),
                ),
                actions=[
                    CupertinoContextMenuAction(
                        trailing_icon=Icons.DELETE,
                        on_click=lambda e, id=reg_id: self.delete_register(id),
                        text="Eliminar Registro",
                    )
                ],
            )

            self.history_page.controls.append(card)

        return self.history_page

    def delete_register(self, reg_id: UUID):
        self.register_manager.delete_register(reg_id)

        self.__build_history_content()
        self.update()

    def __handle_nav(self, e: ControlEvent):
        if not e:
            idx = self.params.private.get("lst_idx")
        else:
            idx = int(e.data)

        self.current_index = idx

        match self.current_index:
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

    def did_mount(self):
        if self.params.private.get("lst_idx", 0):
            self.current_index = self.params.private.get("lst_idx", 0)
            self.__handle_nav(None)
        self.params.private.clear()
        return super().did_mount()
