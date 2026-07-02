from flet import (
    Colors,
    Column,
    Container,
    FontWeight,
    Row,
    Text,
    TextSpan,
    TextStyle,
)

from utils.get_color_by_value import get_color_by_value


class DetailCardTag(Container):
    def __init__(self, tag_text: str, bgcolor: Colors, text_color: Colors):
        super().__init__()
        self.tag_text = tag_text
        self.bgcolor = bgcolor
        self.text_color = text_color
        self.content = Row(
            controls=[
                Text(
                    self.tag_text,
                    size=13,
                    color=self.text_color
                ),
            ],
            tight=True,
            spacing=5,
        )
        self.padding = 5
        self.border_radius = 20


class DetailCard(Container):
    def __init__(self, value: float | str | None = 0, date: str | None = None):
        super().__init__()
        self.value = value
        self.date = date
        self.text, self.bgcolor, self.text_color = get_color_by_value(self.value)
        self.content = Row(
            controls=[
                Column(
                    controls=[
                        Text(
                            value="TSH",
                            color=Colors.WHITE,
                            size=16,
                            weight=FontWeight.BOLD,
                        ),
                        Text(
                            value=self.value,
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
                        DetailCardTag(self.text, self.bgcolor, self.text_color),
                        Container(
                            content=Text(
                                self.date,
                                color=Colors.WHITE,
                            )
                        ),
                    ]
                ),
            ]
        )
        self.padding = 15
        self.bgcolor = Colors.DEEP_PURPLE_ACCENT_200
        self.border_radius = 20
