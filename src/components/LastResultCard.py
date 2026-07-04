from flet import (
    Colors,
    Column,
    Container,
    FontWeight,
    Icon,
    Icons,
    MainAxisAlignment,
    Row,
    Text,
    TextSpan,
    TextStyle,
)


class LastResultCard(Container):
    def __init__(self, hormone: str, value: float, date: str):
        super().__init__()
        self.content = Column(
            controls=[
                Text(
                    value="Último Resultado",
                    color=Colors.WHITE,
                    size=15,
                ),
                Text(
                    value=hormone,
                    color=Colors.WHITE,
                    size=16,
                    weight=FontWeight.BOLD,
                ),
                Text(
                    value=float(value),
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
                                date,
                                color=Colors.WHITE,
                            )
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
            ]
        )
        self.padding = 15
        self.bgcolor = Colors.DEEP_PURPLE_ACCENT_200
        self.border_radius = 20
