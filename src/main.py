from flet import (
    AppBar,
    BoxShadow,
    ChartAxis,
    ChartAxisLabel,
    ChartGridLines,
    Colors,
    Column,
    Container,
    FontWeight,
    Icon,
    IconButton,
    Icons,
    LineChart,
    LineChartData,
    LineChartDataPoint,
    MainAxisAlignment,
    NavigationBar,
    NavigationBarDestination,
    NavigationDrawer,
    NavigationDrawerDestination,
    Offset,
    Page,
    Row,
    SafeArea,
    ScrollMode,
    Slider,
    Text,
    TextSpan,
    TextStyle,
    ThemeMode,
    app,
    padding,
)


async def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.AUTO

    page.appbar = AppBar(
        title=Text(
            "Tiro",
            size=30,
            weight=FontWeight.BOLD,
            spans=[TextSpan("X", style=TextStyle(color=Colors.DEEP_PURPLE_ACCENT_200))],
        ),
        center_title=True,
        actions=[
            IconButton(
                icon=Icons.NOTIFICATIONS_OUTLINED,
            )
        ],
    )

    page.drawer = NavigationDrawer(
        controls=[
            NavigationDrawerDestination(label="Home", icon=Icons.HOME),
            NavigationDrawerDestination(label="Your Data", icon=Icons.FINGERPRINT),
            NavigationDrawerDestination(label="Settings", icon=Icons.SETTINGS),
        ]
    )

    page.navigation_bar = NavigationBar(
        destinations=[
            NavigationBarDestination(label="Home", icon=Icons.HOME),
            NavigationBarDestination(label="Your Data", icon=Icons.FINGERPRINT),
            NavigationBarDestination(label="Settings", icon=Icons.SETTINGS),
        ]
    )

    page.add(
        SafeArea(
            content=Column(
                controls=[
                    Container(
                        content=Text("Resumen", weight=FontWeight.BOLD, size=16),
                        padding=padding.only(top=30),
                    ),
                    Container(
                        content=Column(
                            controls=[
                                Text(
                                    value="Último Resultado",
                                    color=Colors.WHITE,
                                    size=15,
                                ),
                                Text(
                                    value="TSH",
                                    color=Colors.WHITE,
                                    size=16,
                                    weight=FontWeight.BOLD,
                                ),
                                Text(
                                    value="2.18",
                                    color=Colors.WHITE,
                                    size=28,
                                    weight=FontWeight.BOLD,
                                    spans=[
                                        TextSpan(
                                            " m Ul/L",
                                            style=TextStyle(size=10),
                                        )
                                    ],
                                ),
                                Row(
                                    controls=[
                                        Container(
                                            content=Row(
                                                controls=[
                                                    Icon(
                                                        Icons.CHECK,
                                                        size=13,
                                                        color=Colors.WHITE,
                                                    ),
                                                    Text(
                                                        "Normal",
                                                        size=13,
                                                        color=Colors.WHITE,
                                                    ),
                                                ],
                                                tight=True,
                                                spacing=5,
                                            ),
                                            padding=5,
                                            bgcolor=Colors.GREEN_300,
                                            border_radius=20,
                                        ),
                                        Container(
                                            content=Text(
                                                "20 may 2024", color=Colors.WHITE
                                            )
                                        ),
                                    ],
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ]
                        ),
                        padding=15,
                        bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                        border_radius=20,
                    ),
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
                                            "0.27 - 4.20 mUI/L", weight=FontWeight.W_400
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
                            blur_radius=1.4, spread_radius=1.3, color=Colors.GREY_300
                        ),
                        bgcolor=Colors.WHITE,
                    ),
                    Container(
                        bgcolor=Colors.WHITE,
                        border_radius=20,
                        padding=20,
                        shadow=BoxShadow(
                            blur_radius=15,
                            color=Colors.BLACK12,
                            offset=Offset(0, 3),
                        ),
                        content=Column(
                            controls=[
                                Text(
                                    "Tus estadísticas",
                                    size=22,
                                    weight=FontWeight.BOLD,
                                ),
                                Text(
                                    "Últimos 6 resultados",
                                    size=14,
                                    color=Colors.GREY_600,
                                ),
                                Container(
                                    height=220,
                                    padding=10,
                                    content=LineChart(
                                        min_x=0,
                                        max_x=5,
                                        min_y=0,
                                        max_y=6,
                                        expand=True,
                                        left_axis=ChartAxis(
                                            labels=[
                                                ChartAxisLabel(
                                                    value=2, label=Text("2")
                                                ),
                                                ChartAxisLabel(
                                                    value=4, label=Text("4")
                                                ),
                                                ChartAxisLabel(
                                                    value=6, label=Text("6")
                                                ),
                                            ],
                                        ),
                                        bottom_axis=ChartAxis(
                                            labels=[
                                                ChartAxisLabel(
                                                    value=0, label=Text("Nov")
                                                ),
                                                ChartAxisLabel(
                                                    value=1, label=Text("Dic")
                                                ),
                                                ChartAxisLabel(
                                                    value=2, label=Text("Ene")
                                                ),
                                                ChartAxisLabel(
                                                    value=3, label=Text("Feb")
                                                ),
                                                ChartAxisLabel(
                                                    value=4, label=Text("Mar")
                                                ),
                                                ChartAxisLabel(
                                                    value=5, label=Text("May")
                                                ),
                                            ],
                                        ),
                                        horizontal_grid_lines=ChartGridLines(
                                            interval=2,
                                            color=Colors.GREY_300,
                                        ),
                                        data_series=[
                                            LineChartData(
                                                color=Colors.DEEP_PURPLE,
                                                stroke_width=3,
                                                curved=True,
                                                data_points=[
                                                    LineChartDataPoint(0, 2.5),
                                                    LineChartDataPoint(1, 4),
                                                    LineChartDataPoint(2, 2.4),
                                                    LineChartDataPoint(3, 3),
                                                    LineChartDataPoint(4, 2),
                                                    LineChartDataPoint(5, 2),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                    Row(
                        controls=[
                            Container(
                                content=Row(
                                    controls=[
                                        Icon(Icons.ADD, color=Colors.WHITE),
                                        Text("Nuevo Registro", color=Colors.WHITE),
                                    ],
                                    tight=True
                                ),
                                bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                                padding=10,
                                border_radius=20,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                ]
            ),
            expand=True,
        )
    )


app(target=main)
