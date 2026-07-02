from typing import Callable

from flet import (
    BoxShadow,
    Colors,
    Column,
    Container,
    FontWeight,
    MainAxisAlignment,
    Row,
    ShadowBlurStyle,
    Text,
    TextSpan,
    TextStyle,
    margin,
    padding,
)

from utils.get_color_by_value import get_color_by_value


class HistoryCardTag(Container):
    def __init__(self, value: float | int | str | None = None):
        super().__init__(
            padding=padding.only(left=10, right=10, top=3, bottom=3), border_radius=20
        )
        self.value = value

    def build(self):
        tag_text, bgcolor, text_color = get_color_by_value(self.value)

        self.content = Text(
            tag_text,
            color=text_color,
            weight=FontWeight.BOLD,
        )

        self.bgcolor = bgcolor
        return super().build()


class HistoryCard(Container):
    def __init__(
        self,
        on_click: Callable[[any], None] | None = None,
        value: float | str | None = None,
        date: str | None = None,
    ):
        super().__init__()
        self.value = value
        self.date = date
        self.value_text, self.card_bgcolor, self.text_color = get_color_by_value(
            self.value
        )
        self.content = Column(
            controls=[
                Row(
                    controls=[
                        Text("TSH", size=19, weight=FontWeight.W_500),
                        Text(
                            self.value,
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
                        Text(self.date),
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
        self.bgcolor = Colors.WHITE
        self.margin = margin.all(10)
        self.on_click = on_click
        self.ink = True
