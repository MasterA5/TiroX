from flet import (
    Colors,
    ColorValue,
    Column,
    Container,
    Control,
    FontWeight,
    Icon,
    Icons,
    IconValue,
    OptionalControlEventCallable,
    Row,
    Text,
    alignment,
    padding,
)


class SettingsCard(Container):
    def __init__(
        self,
        icon: IconValue | None = None,
        icon_color: ColorValue | None = Colors.DEEP_PURPLE_ACCENT_200,
        title: str | None = None,
        subtitle: str | None = None,
        action: Control | None = None,
        on_click: OptionalControlEventCallable = None,
    ):
        super().__init__()
        self.border_radius = 20
        self.bgcolor = Colors.SURFACE
        self.ink = self.on_click is not None
        self.alignment = alignment.center
        self.icon = Icon(
            icon,
            color=icon_color,
        )
        self.icon_color = icon_color
        self.title = title
        self.subtitle = subtitle
        self.content = Row(
            controls=[
                Container(
                    width=46,
                    height=46,
                    border_radius=23,
                    bgcolor=Colors.with_opacity(0.12, self.icon_color),
                    alignment=alignment.center,
                    content=self.icon,
                ),
                Container(
                    content=Column(
                        spacing=2,
                        controls=[
                            Text(
                                self.title,
                                size=17,
                                weight=FontWeight.W_600,
                            ),
                            Text(
                                self.subtitle,
                                color=Colors.GREY_500,
                                size=13,
                                visible=subtitle is not None,
                            ),
                        ],
                    ),
                    expand=True,
                ),
                Container(
                    content=Icon(
                        Icons.ARROW_FORWARD_IOS_ROUNDED,
                        size=18,
                        color=Colors.GREY_500,
                        visible=action is None,
                    ),
                    padding=padding.only(right=10),
                ),
                Container(content=action, visible=action is not None),
            ]
        )
        self.on_click = on_click


class SettingsCardSection(Container):
    def __init__(
        self,
        text: str | None = None,
        sections: list[SettingsCard] | None = None,
    ):
        super().__init__()
        self.padding = padding.only(left=10)
        self.content = Column(
            controls=[
                Row(
                    controls=[
                        Text(
                            text.upper(),
                            size=13,
                            color=Colors.DEEP_PURPLE_ACCENT_200,
                            weight=FontWeight.BOLD,
                        ),
                    ]
                ),
                Column(
                    controls=sections if sections else [],
                    spacing=30,
                    expand=True,
                ),
            ]
        )
