from flet import (
    Colors,
    Column,
    Container,
    CrossAxisAlignment,
    FontWeight,
    Icon,
    Icons,
    MainAxisAlignment,
    Row,
    Text,
    TextAlign,
    alignment,
)


class NotificationCard(Container):
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        icon_color: str = Colors.DEEP_PURPLE_ACCENT_200,
        time: str | None = None,
        unread: bool = False,
    ):
        super().__init__(
            bgcolor=Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=20,
            padding=18,
            content=Row(
                spacing=15,
                vertical_alignment=CrossAxisAlignment.START,
                controls=[
                    Container(
                        width=50,
                        height=50,
                        border_radius=25,
                        bgcolor=icon_color,
                        alignment=alignment.center,
                        content=Icon(
                            icon,
                            color=Colors.WHITE,
                            size=26,
                        ),
                    ),
                    Column(
                        expand=True,
                        spacing=5,
                        controls=[
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text(
                                        title,
                                        size=17,
                                        weight=FontWeight.BOLD,
                                        expand=True,
                                    ),
                                    Text(
                                        time or "",
                                        size=12,
                                        color=Colors.GREY_500,
                                    ),
                                ],
                            ),
                            Text(
                                description,
                                size=14,
                                color=Colors.GREY_500,
                            ),
                        ],
                    ),
                    Container(
                        width=10,
                        height=10,
                        border_radius=5,
                        bgcolor=Colors.DEEP_PURPLE_ACCENT_200
                        if unread
                        else Colors.TRANSPARENT,
                    ),
                ],
            ),
        )


class EmptyNotifications(Container):
    def __init__(self):
        super().__init__(
            expand=True,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    Container(
                        width=90,
                        height=90,
                        border_radius=45,
                        bgcolor=Colors.DEEP_PURPLE_ACCENT_100,
                        alignment=alignment.center,
                        content=Icon(
                            Icons.NOTIFICATIONS_NONE_ROUNDED,
                            size=48,
                            color=Colors.DEEP_PURPLE_ACCENT_700,
                        ),
                    ),
                    Text(
                        "No tienes notificaciones",
                        size=24,
                        weight=FontWeight.BOLD,
                    ),
                    Text(
                        "Cuando ocurra algún evento importante\naparecerá aquí.",
                        text_align=TextAlign.CENTER,
                        color=Colors.GREY_500,
                    ),
                ],
            ),
        )
