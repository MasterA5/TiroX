from flet import (
    BoxShadow,
    Colors,
    Column,
    Container,
    FontWeight,
    IconButton,
    Icons,
    MainAxisAlignment,
    Row,
    Slider,
    Text,
)


class RangeCard(Container):
    def __init__(self):
        super().__init__()
        self.content = Column(
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
                            "0.27 mUI/L - 4.20 mUI/L",
                            weight=FontWeight.W_400,
                        ),
                    ],
                    spacing=3,
                ),
                Container(height=3),
                Slider(),
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
