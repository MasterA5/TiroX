import datetime
from typing import Callable

from flet import (
    BoxShadow,
    Colors,
    ColorValue,
    Column,
    Container,
    FontWeight,
    Icon,
    Icons,
    MainAxisAlignment,
    Row,
    ShadowBlurStyle,
    Text,
    TextSpan,
    TextStyle,
    ThemeMode,
    margin,
    padding,
)

from utils.formater import Formater
from utils.get_color_by_value import get_color_by_value
from utils.get_icon_by_value import get_icon_by_value
from utils.get_text_by_value import get_text_by_value


class HistoryCardTag(Container):
    def __init__(self, value: float | int | str | None = None):
        super().__init__(
            padding=padding.only(left=10, right=10, top=3, bottom=3), border_radius=20
        )
        self.value = value

    def build(self):
        tag_text = get_text_by_value(self.value)
        bgcolor, text_color = get_color_by_value(self.value)
        icon = get_icon_by_value(self.value)

        self.content = Row(
            controls=[
                Icon(name=icon, color=text_color, size=15),
                Text(
                    tag_text,
                    color=text_color,
                    weight=FontWeight.BOLD,
                ),
            ],
            spacing=4,
        )

        self.bgcolor = bgcolor
        return super().build()


class HistoryCard(Container):
    def __init__(
        self,
        on_click: Callable[[any], None] | None = None,
        value: float | str | None = None,
        date: str | datetime.datetime | None = None,
        icon_color: ColorValue = Colors.DEEP_PURPLE_ACCENT_200,
    ):
        super().__init__()
        self.value = value
        self.date = date
        self.value_text = get_text_by_value(self.value)
        self.card_bgcolor, self.text_color = get_color_by_value(self.value)
        self.icon_color = icon_color
        self.formated_date, self.formated_hour = Formater.format_datetime(
            str(self.date)
        )
        self.content = Column(
            controls=[
                Row(
                    controls=[
                        Text("TSH", size=19, weight=FontWeight.W_500),
                        Text(
                            f"{self.value:.2f}",
                            color=self.text_color,
                            size=20,
                            weight=FontWeight.BOLD,
                            spans=[
                                TextSpan(
                                    " mUI/L",
                                    style=TextStyle(color=self.text_color, size=10),
                                )
                            ],
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
                Row(
                    controls=[
                        Column(
                            controls=[
                                Row(
                                    controls=[
                                        Row(
                                            controls=[
                                                Icon(
                                                    Icons.CALENDAR_MONTH,
                                                    size=20,
                                                    color=self.icon_color,
                                                ),
                                                Text(self.formated_date),
                                            ],
                                            spacing=3,
                                        ),
                                    ]
                                ),
                                Row(
                                    controls=[
                                        Icon(
                                            Icons.ACCESS_TIME,
                                            size=20,
                                            color=self.icon_color,
                                        ),
                                        Text(self.formated_hour),
                                    ],
                                    spacing=3,
                                ),
                            ]
                        ),
                        HistoryCardTag(self.value),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
            ]
        )
        self.padding = 20
        self.border_radius = 20
        self.shadow = BoxShadow(
            spread_radius=1.12,
            blur_radius=1.12,
            blur_style=ShadowBlurStyle.OUTER,
        )
        self.margin = margin.all(10)
        self.on_click = on_click
        self.ink = True

    def build(self):
        self.bgcolor = (
            Colors.SURFACE
            if self.page.theme_mode == ThemeMode.LIGHT
            else Colors.DEEP_PURPLE_900
        )
        return super().build()
