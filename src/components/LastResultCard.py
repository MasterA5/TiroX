from flet import (
    Colors,
    Column,
    Container,
    FontWeight,
    Icon,
    MainAxisAlignment,
    Row,
    Text,
    TextSpan,
    TextStyle,
)

from utils.formater import Formater
from utils.get_color_by_value import get_color_by_value
from utils.get_icon_by_value import get_icon_by_value


class LastResultCardTag(Container):
    def __init__(self, value: float | int | str):
        super().__init__()
        self.value = value
        self.tag_text, self.bgcolor, self.text_color = get_color_by_value(
            float(self.value),
            bg_custom_colors=[
                Colors.LIGHT_GREEN_ACCENT_700,
                Colors.AMBER_600,
                Colors.RED,
            ],
            txt_custom_colors=[
                Colors.LIGHT_GREEN_50,
                Colors.YELLOW_100,
                Colors.RED_50,
            ],
        )
        self.icon = get_icon_by_value(float(self.value))
        self.content = Row(
            controls=[
                Icon(
                    self.icon,
                    size=15,
                    color=self.text_color,
                ),
                Text(
                    self.tag_text,
                    size=13,
                    color=self.text_color,
                ),
            ],
            tight=True,
            spacing=5,
        )
        self.padding = 5
        self.border_radius = 20


class LastResultCard(Container):
    def __init__(self, hormone: str, value: float, date: str):
        super().__init__()
        self.value = value
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
                        LastResultCardTag(self.value),
                        Container(
                            content=Text(
                                Formater.format_datetime(str(date), legible=True),
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
