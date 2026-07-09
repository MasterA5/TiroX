from flet import (
    BoxShadow,
    Colors,
    Column,
    Container,
    FontWeight,
    Icon,
    IconButton,
    Icons,
    MainAxisAlignment,
    Row,
    Text,
)

from utils.get_color_by_value import get_color_by_value
from utils.get_icon_by_value import get_icon_by_value
from utils.get_text_by_value import get_text_by_value


class RangeCard(Container):
    def __init__(self, value: float):
        super().__init__()
        self.value = value
        self.text = get_text_by_value(
            value=self.value,
            texts=["En Rango Normal", "En Rango Limite", "En Rango Alto"],
        )
        self.icon = get_icon_by_value(
            value=self.value,
            icons=[
                Icons.CHECK_OUTLINED,
                Icons.WARNING_OUTLINED,
                Icons.ERROR_OUTLINE
            ],
        )
        self.state_bgcolor, self.state_text_color = get_color_by_value(self.value)
        self.content = Column(
            controls=[
                Column(
                    controls=[
                        Row(
                            controls=[
                                Text(
                                    "Estado",
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
                        Row(
                            controls=[
                                Container(
                                    content=Row(
                                        controls=[
                                            Container(
                                                content=Icon(
                                                    self.icon,
                                                    color=self.state_text_color,
                                                ),
                                                padding=10,
                                                bgcolor=self.state_bgcolor,
                                                border_radius=20,
                                                visible=self.icon is not None,
                                            ),
                                            Row(
                                                controls=[
                                                    Text(
                                                        value=self.text,
                                                        color=self.state_text_color,
                                                        size=16,
                                                        weight=FontWeight.BOLD,
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    padding=10,
                                )
                            ],
                        ),
                    ]
                ),
                Container(height=3, bgcolor=Colors.GREY_200),
                Row(
                    controls=[
                        Column(
                            controls=[
                                Text(
                                    "Rango de referencia",
                                    weight=FontWeight.W_500,
                                ),
                                Text(
                                    "0.27 mUI/L - 4.20 mUI/L",
                                    weight=FontWeight.W_400,
                                ),
                            ],
                            spacing=3,
                            visible=self.value > 0,
                        ),
                        Column(
                            controls=[
                                Text(
                                    "Tus Resultados",
                                    weight=FontWeight.W_500,
                                ),
                                Text(
                                    f"{self.value} mUI/L",
                                    weight=FontWeight.W_400,
                                ),
                            ],
                            spacing=3,
                            visible=self.value > 0,
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
            ]
        )
        self.padding = 15
        self.border_radius = 20
        self.shadow = BoxShadow(
            blur_radius=1.4,
            spread_radius=1.3,
            color=Colors.GREY_300,
        )
        self.bgcolor = Colors.WHITE
