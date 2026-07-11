from typing import Callable

from flet import (
    Colors,
    Container,
    Control,
    FontWeight,
    Icon,
    Icons,
    MainAxisAlignment,
    Row,
    Text,
)


class StylishButton(Container):
    def __init__(
        self,
        text: str,
        on_click: Callable[[any], None] | None = None,
        bgcolor: Colors = Colors.DEEP_PURPLE_ACCENT_200,
        text_color: Colors = Colors.WHITE,
        border_radius: int = 10,
        icon: Icons | None = None,
        content: Control | None = None
    ):
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.bgcolor = bgcolor
        self.icon = icon
        self.text_color = text_color
        self.padding = 16
        self.border_radius = border_radius
        self.content = Row(
            controls=[
                Icon(self.icon, color=self.text_color, visible=self.icon is not None),
                Text(self.text, color=self.text_color, weight=FontWeight.BOLD),
            ],
            alignment=MainAxisAlignment.CENTER,
        ) if not content else content
        self.expand = True
        self.ink = True
