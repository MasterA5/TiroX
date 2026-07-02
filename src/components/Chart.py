from flet import (
    BoxShadow,
    ChartAxis,
    ChartAxisLabel,
    ChartGridLines,
    Colors,
    Column,
    Container,
    FontWeight,
    LineChart,
    LineChartData,
    LineChartDataPoint,
    Offset,
    Text,
)


class TiroXChart(Container):
    def __init__(self):
        super().__init__()
        self.bgcolor = Colors.WHITE
        self.border_radius = 20
        self.padding = 20
        self.shadow = BoxShadow(
            blur_radius=15,
            color=Colors.BLACK12,
            offset=Offset(0, 3),
        )
        self.content = Column(
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
                                ChartAxisLabel(value=1, label=Text("1")),
                                ChartAxisLabel(value=2, label=Text("2")),
                                ChartAxisLabel(value=3, label=Text("3")),
                                ChartAxisLabel(value=4, label=Text("4")),
                                ChartAxisLabel(value=5, label=Text("5")),
                            ],
                        ),
                        bottom_axis=ChartAxis(
                            labels=[
                                ChartAxisLabel(value=0, label=Text("Nov")),
                                ChartAxisLabel(value=1, label=Text("Dic")),
                                ChartAxisLabel(value=2, label=Text("Ene")),
                                ChartAxisLabel(value=3, label=Text("Feb")),
                                ChartAxisLabel(value=4, label=Text("Mar")),
                                ChartAxisLabel(value=5, label=Text("May")),
                            ]
                        ),
                        horizontal_grid_lines=ChartGridLines(
                            interval=2,
                            color=Colors.GREY_300,
                        ),
                        data_series=[
                            LineChartData(
                                color=Colors.DEEP_PURPLE_ACCENT_200,
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
        )
