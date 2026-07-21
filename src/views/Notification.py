from flet import (
    AppBar,
    Colors,
    Column,
    Container,
    FontWeight,
    IconButton,
    Icons,
    SafeArea,
    ScrollMode,
    Text,
    View,
)
from flet_routing import FletRouter, Params

from components.NotificationCard import EmptyNotifications, NotificationCard


class NotificationsView(View):
    def __init__(self, params: Params):
        super().__init__("/notifications")
        self.router: FletRouter = params.router
        self.lst_idx = params.private.get("lst_idx", 0)

        self.appbar = AppBar(
            title=Text(
                "Notificaciones",
                weight=FontWeight.BOLD,
            ),
            center_title=True,
            leading=IconButton(
                Icons.ARROW_BACK,
                on_click=lambda e: self.router.replace(
                    path="/",
                    private_params={
                        "lst_idx": self.lst_idx,
                    },
                ),
            ),
        )

        # Cambiar por False cuando tengas datos reales
        has_notifications = True

        self.controls = [
            SafeArea(
                expand=True,
                content=Container(
                    padding=20,
                    content=(
                        Column(
                            scroll=ScrollMode.AUTO,
                            spacing=18,
                            controls=[
                                Column(
                                    spacing=4,
                                    controls=[
                                        Text(
                                            "Centro de Notificaciones",
                                            size=30,
                                            weight=FontWeight.BOLD,
                                        ),
                                        Text(
                                            "Mantente informado sobre tus análisis y novedades.",
                                            color=Colors.GREY_500,
                                        ),
                                    ],
                                ),
                                NotificationCard(
                                    title="Nuevo análisis registrado",
                                    description="Tu último resultado fue guardado correctamente.",
                                    icon=Icons.SCIENCE_OUTLINED,
                                    time="Hace 5 min",
                                    unread=True,
                                ),
                                NotificationCard(
                                    title="Recordatorio",
                                    description="No olvides registrar tu próximo análisis.",
                                    icon=Icons.EVENT_AVAILABLE_OUTLINED,
                                    icon_color=Colors.BLUE_400,
                                    time="Ayer",
                                ),
                                NotificationCard(
                                    title="Bienvenido a TiroX",
                                    description="Gracias por utilizar nuestra aplicación.",
                                    icon=Icons.FAVORITE_OUTLINED,
                                    icon_color=Colors.PINK_300,
                                    time="Hace 3 días",
                                ),
                            ],
                        )
                        if has_notifications
                        else EmptyNotifications()
                    ),
                ),
            )
        ]
