from uuid import UUID

from flet import (
    AppBar,
    Colors,
    Column,
    Container,
    ControlEvent,
    CrossAxisAlignment,
    CupertinoContextMenu,
    CupertinoContextMenuAction,
    FontWeight,
    Icon,
    IconButton,
    Icons,
    ListView,
    MainAxisAlignment,
    NavigationBar,
    NavigationBarDestination,
    NavigationBarLabelBehavior,
    NavigationDrawer,
    NavigationDrawerDestination,
    Row,
    SafeArea,
    Switch,
    Text,
    TextSpan,
    TextStyle,
    ThemeMode,
    View,
    alignment,
    padding,
)
from flet_routing import FletRouter, Params

from components.AnimatedIcon import RotatingSettingsWheel
from components.HistoryCard import HistoryCard
from components.LastResultCard import LastResultCard
from components.RangeCard import RangeCard
from components.SettingCardSection import SettingsCard, SettingsCardSection
from components.StylishButton import StylishButton
from components.StylishSnackBar import RegisterDeletedSuccefull
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
                NavigationDrawerDestination(label="Inicio", icon=Icons.HOME),
                NavigationDrawerDestination(label="Historial", icon=Icons.FINGERPRINT),
                NavigationDrawerDestination(label="Configuracion", icon=Icons.SETTINGS),
            ],
            on_change=self.__handle_nav,
            tile_padding=23,
        )
        self.navigation_bar = NavigationBar(
            destinations=[
                NavigationBarDestination(label="Inicio", icon=Icons.HOME),
                NavigationBarDestination(label="Historial", icon=Icons.FINGERPRINT),
                NavigationBarDestination(label="Configuracion", icon=Icons.SETTINGS),
            ],
            on_change=self.__handle_nav,
            label_behavior=NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        )
        self.main_container = SafeArea(content=self.__build_home_content(), expand=True)
        self.controls = [self.main_container]
        self.scroll = "auto"
        self.expand = True
        self.current_index = 0
        self.history_list = ListView(
            controls=[],
            expand=True,
            spacing=10,
        )
        self.history_page = Column(
            controls=[
                self.history_list,
            ],
            expand=True,
            scroll="auto",
        )

    def __build_home_content(self):
        last_register = self.register_manager.get_last_register()

        if last_register:
            last_result_card = LastResultCard(
                hormone=last_register.hormone,
                value=last_register.value,
                date=last_register.date,
            )
            range_card = RangeCard(last_register.value)
        else:
            last_result_card = Container(
                height=170,
                border_radius=25,
                bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                alignment=alignment.center,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Icon(
                            Icons.INSERT_CHART_OUTLINED,
                            size=60,
                            color=Colors.WHITE,
                        ),
                        Text(
                            "Todavía no hay registros",
                            size=22,
                            weight=FontWeight.BOLD,
                            color=Colors.WHITE,
                        ),
                        Text(
                            "Agrega tu primer análisis para comenzar.",
                            color=Colors.WHITE70,
                        ),
                    ],
                ),
            )

            range_card = RangeCard(0)

        return Column(
            scroll="auto",
            spacing=24,
            controls=[
                Container(
                    padding=padding.only(left=10, right=10, top=10),
                    content=Column(
                        spacing=2,
                        controls=[
                            Text(
                                "Bienvenido 👋",
                                size=15,
                                color=Colors.GREY_500,
                            ),
                            Text(
                                "Resumen",
                                size=32,
                                weight=FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
                last_result_card,
                range_card,
                Container(
                    padding=padding.only(left=5),
                    content=Text(
                        "Acciones rápidas",
                        size=18,
                        weight=FontWeight.BOLD,
                    ),
                ),
                Row(
                    spacing=15,
                    controls=[
                        Container(
                            StylishButton(
                                on_click=lambda e: self.router.push("/create/register"),
                                text="Nuevo Registro",
                                icon=Icons.ADD,
                                bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                            ),
                            expand=True,
                        ),
                        Container(
                            StylishButton(
                                on_click=lambda e: self.__handle_nav(
                                    ControlEvent(
                                        target="",
                                        name="change",
                                        data="1",
                                        control=None,
                                        page=self.page,
                                    )
                                ),
                                text="Historial",
                                icon=Icons.HISTORY,
                                bgcolor=Colors.BLUE_400,
                            ),
                            expand=True,
                        ),
                    ],
                ),
            ],
        )

    def __build_history_content(self):
        self.history_list.controls.clear()
        registers = self.register_manager.get_all_registers()

        if not registers:
            self.history_list.controls.append(
                Container(
                    expand=True,
                    alignment=alignment.center,
                    content=Column(
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
                                        on_click=lambda e: self.router.push(
                                            "/create/register", {"lst_idx": 1}
                                        ),
                                    ),
                                ],
                                width=230,
                            ),
                        ],
                    ),
                )
            )

            return Column(
                expand=True,
                spacing=20,
                controls=[
                    Container(
                        content=Column(
                            spacing=4,
                            controls=[
                                Text(
                                    "Historial",
                                    size=30,
                                    weight=FontWeight.BOLD,
                                ),
                                Text(
                                    "Todos tus análisis ordenados por fecha.",
                                    color=Colors.GREY_500,
                                ),
                            ],
                        ),
                    ),
                    self.history_list,
                ],
            )

        for register in registers:
            reg_id = register.id
            reg_value = register.value
            reg_date = register.date

            card = CupertinoContextMenu(
                content=HistoryCard(
                    on_click=lambda e, id=reg_id: self.router.push(
                        f"/detail/{id}",
                        {"lst_idx": 1},
                    ),
                    value=float(reg_value),
                    date=reg_date,
                ),
                actions=[
                    CupertinoContextMenuAction(
                        text="Eliminar registro",
                        trailing_icon=Icons.DELETE,
                        is_destructive_action=True,
                        on_click=lambda e, id=reg_id: self.delete_register(id),
                    ),
                ],
            )

            self.history_list.controls.append(card)

        return Column(
            expand=True,
            spacing=18,
            controls=[
                Container(
                    content=Column(
                        spacing=4,
                        controls=[
                            Text(
                                "Historial",
                                size=30,
                                weight=FontWeight.BOLD,
                            ),
                            Text(
                                f"{len(registers)} registros encontrados",
                                color=Colors.GREY_500,
                                size=15,
                            ),
                            Container(height=2, bgcolor=Colors.GREY_200),
                        ],
                    ),
                ),
                self.history_list,
            ],
        )

    def __build_settings_content(self):
        return Column(
            expand=True,
            scroll="auto",
            spacing=25,
            controls=[
                Container(
                    content=Column(
                        spacing=5,
                        controls=[
                            Row(
                                controls=[
                                    RotatingSettingsWheel(36),
                                    Text(
                                        "Configuración",
                                        size=30,
                                        weight=FontWeight.BOLD,
                                    ),
                                ]
                            ),
                            Text(
                                "Personaliza Tu Experiencia",
                                color=Colors.GREY_500,
                            ),
                        ],
                    ),
                ),
                SettingsCardSection(
                    text="General",
                    sections=[
                        SettingsCard(
                            icon=Icons.LIGHT_MODE
                            if self.page.theme_mode != ThemeMode.DARK
                            else Icons.DARK_MODE,
                            title="Tema",
                            action=Switch(
                                inactive_thumb_color=Colors.DEEP_PURPLE_ACCENT_200,
                                active_color=Colors.DEEP_PURPLE_ACCENT_200,
                                on_change=lambda e: (
                                    setattr(
                                        self.page,
                                        "theme_mode",
                                        ThemeMode.DARK
                                        if self.page.theme_mode != ThemeMode.DARK
                                        else ThemeMode.LIGHT,
                                    ),
                                    setattr(
                                        e.control.parent.parent.parent.icon,
                                        "name",
                                        Icons.DARK_MODE
                                        if self.page.theme_mode == ThemeMode.DARK
                                        else Icons.LIGHT_MODE,
                                    ),
                                    e.control.parent.update(),
                                    self.page.update(),
                                ),
                                value=False
                                if self.page.theme_mode != ThemeMode.DARK
                                else True,
                            ),
                        ),
                        SettingsCard(
                            icon=Icons.NOTIFICATIONS_OUTLINED,
                            title="Notificaciones",
                            action=Switch(
                                thumb_color=Colors.DEEP_PURPLE_ACCENT_200,
                                active_color=Colors.DEEP_PURPLE_ACCENT_200,
                            ),
                        ),
                    ],
                ),
                SettingsCardSection(
                    text="Datos",
                    sections=[
                        SettingsCard(
                            icon=Icons.IOS_SHARE,
                            title="Exporta Tus Registros",
                            subtitle="Exporta Una Copia De Tus Registros",
                        ),
                        SettingsCard(
                            icon=Icons.SYNC,
                            title="Sincroniza Tus Registros",
                            subtitle="Sincroniza Tus Registros Para Estar Al Dia",
                        ),
                        SettingsCard(
                            icon=Icons.DELETE_FOREVER_OUTLINED,
                            title="Eliminar Todo Tus Registros",
                            icon_color=Colors.RED_400,
                        ),
                    ],
                ),
                SettingsCardSection(
                    text="Información",
                    sections=[
                        SettingsCard(
                            icon=Icons.INFO_OUTLINE,
                            title="Acerca de",
                        ),
                        SettingsCard(
                            icon=Icons.FAVORITE_OUTLINE,
                            title="Versión",
                            subtitle="1.0.0",
                        ),
                    ],
                ),
            ],
        )

    def delete_register(self, reg_id: UUID):
        self.register_manager.delete_register(reg_id)

        self.__build_history_content()
        self.page.open(RegisterDeletedSuccefull())
        self.update()

    def __handle_nav(self, e: ControlEvent):
        if e is None:
            idx = self.params.private.get("lst_idx", 0)
        else:
            idx = int(e.data)

        if idx == self.current_index:
            return

        self.current_index = idx
        self.__show_page(idx)

    def __show_page(self, idx: int) -> int:
        match self.current_index:
            case 0:
                self.main_container.content = self.__build_home_content()
            case 1:
                self.main_container.content = self.__build_history_content()
            case 2:
                self.main_container.content = self.__build_settings_content()

        self.navigation_bar.selected_index = idx
        self.drawer.selected_index = idx

        self.main_container.update()

    def did_mount(self):
        idx = self.params.private.get("lst_idx")

        if idx is not None:
            self.current_index = idx
            self.__show_page(idx)

        self.params.private.clear()

        return super().did_mount()
