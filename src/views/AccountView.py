import os
from pathlib import Path

from flet import (
    AppBar,
    Colors,
    Column,
    Container,
    ControlEvent,
    CrossAxisAlignment,
    FontWeight,
    Icon,
    IconButton,
    Icons,
    MainAxisAlignment,
    Row,
    Text,
    View,
    alignment,
    border,
    padding,
)
from flet_routing import FletRouter, Params

from components.StylishButton import StylishButton
from core.AuthManager import TiroxAuthManager


class AccountView(View):
    def __init__(self, params: Params, auth_manager: TiroxAuthManager | None = None):
        super().__init__("/account")

        self.params = params
        self.router: FletRouter = self.params.router
        self.auth_manager = auth_manager
        self.scroll = "auto"

        user = auth_manager.get_current_user() if auth_manager else None
        display_name = (user or {}).get("username") or "Usuario"
        display_email = (user or {}).get("email") or "usuario@email.com"

        # ---------------------------------------------------------
        # APP BAR
        # ---------------------------------------------------------

        self.appbar = AppBar(
            title=Text(
                "Mi cuenta",
                size=17,
                weight=FontWeight.W_700,
            ),
            leading=IconButton(
                icon=Icons.ARROW_BACK,
                on_click=lambda e: self.router.replace(
                    "/",
                    {"lst_idx": self.params.private.get("lst_idx", 1)},
                ),
            ),
            center_title=True,
            bgcolor=Colors.WHITE,
        )

        # ---------------------------------------------------------
        # PROFILE
        # ---------------------------------------------------------

        profile_card = Row(
            controls=[
                Container(
                    bgcolor=Colors.WHITE,
                    border=border.all(
                        1,
                        Colors.GREY_200,
                    ),
                    border_radius=22,
                    padding=22,
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            Container(
                                width=90,
                                height=90,
                                bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                                border_radius=45,
                                alignment=alignment.center,
                                content=Icon(
                                    Icons.PERSON_OUTLINE,
                                    size=48,
                                    color=Colors.WHITE,
                                ),
                            ),
                            Text(
                                display_name,
                                size=22,
                                weight=FontWeight.W_700,
                            ),
                            Text(
                                "Gestiona tu información personal",
                                size=13,
                                color=Colors.GREY_600,
                                text_align="center",
                            ),
                        ],
                    ),
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        )

        account_info = Container(
            bgcolor=Colors.WHITE,
            border=border.all(
                1,
                Colors.GREY_200,
            ),
            border_radius=22,
            padding=20,
            content=Column(
                spacing=0,
                controls=[
                    Row(
                        spacing=12,
                        controls=[
                            Container(
                                width=44,
                                height=44,
                                bgcolor=Colors.DEEP_PURPLE_50,
                                border_radius=12,
                                alignment=alignment.center,
                                content=Icon(
                                    Icons.PERSON_OUTLINE,
                                    size=23,
                                    color=Colors.DEEP_PURPLE_ACCENT_200,
                                ),
                            ),
                            Column(
                                spacing=2,
                                controls=[
                                    Text(
                                        "Información personal",
                                        size=16,
                                        weight=FontWeight.W_700,
                                    ),
                                    Text(
                                        "Datos asociados a tu cuenta",
                                        size=12,
                                        color=Colors.GREY_600,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(height=20),
                    self.__info_row(
                        Icons.PERSON,
                        "Nombre",
                        display_name,
                    ),
                    Container(height=12),
                    self.__info_row(
                        Icons.EMAIL_OUTLINED,
                        "Correo electrónico",
                        display_email,
                    ),
                ],
            ),
        )

        security = Container(
            bgcolor=Colors.WHITE,
            border=border.all(
                1,
                Colors.GREY_200,
            ),
            border_radius=22,
            padding=20,
            content=Column(
                spacing=0,
                controls=[
                    Row(
                        spacing=12,
                        controls=[
                            Container(
                                width=44,
                                height=44,
                                bgcolor=Colors.GREY_100,
                                border_radius=12,
                                alignment=alignment.center,
                                content=Icon(
                                    Icons.SECURITY_OUTLINED,
                                    size=23,
                                    color=Colors.DEEP_PURPLE_ACCENT_200,
                                ),
                            ),
                            Column(
                                spacing=2,
                                controls=[
                                    Text(
                                        "Seguridad",
                                        size=16,
                                        weight=FontWeight.W_700,
                                    ),
                                    Text(
                                        "Protege tu cuenta",
                                        size=12,
                                        color=Colors.GREY_600,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(height=18),
                    self.__action_row(
                        Icons.LOCK_OUTLINE,
                        "Cambiar contraseña",
                        "Actualiza tu contraseña",
                    ),
                ],
            ),
        )

        logout = Container(
            bgcolor=Colors.RED_50,
            border_radius=18,
            padding=12,
            content=Row(
                controls=[
                    StylishButton(
                        text="Cerrar sesión",
                        icon=Icons.LOGOUT,
                        bgcolor=Colors.RED_400,
                        on_click=self.__handle_logout,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
        )

        self.controls = [
            Container(
                padding=padding.only(
                    left=20,
                    right=20,
                    top=22,
                    bottom=40,
                ),
                content=Column(
                    spacing=18,
                    controls=[
                        profile_card,
                        account_info,
                        security,
                        Container(height=2),
                        logout,
                        Row(
                            spacing=6,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Icon(
                                    Icons.LOCK_OUTLINE,
                                    size=14,
                                    color=Colors.GREY_500,
                                ),
                                Text(
                                    "Tu información está protegida",
                                    size=11,
                                    color=Colors.GREY_500,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        ]

    def __handle_logout(self, e):
        if self.auth_manager:
            self.auth_manager.logout()

        self.router.replace("/")

    def __info_row(
        self,
        icon,
        title,
        value,
    ):
        return Container(
            bgcolor=Colors.GREY_50,
            border_radius=15,
            padding=12,
            content=Row(
                spacing=12,
                controls=[
                    Icon(
                        icon,
                        size=21,
                        color=Colors.GREY_600,
                    ),
                    Column(
                        spacing=2,
                        expand=True,
                        controls=[
                            Text(
                                title,
                                size=11,
                                color=Colors.GREY_600,
                            ),
                            Text(
                                value,
                                size=14,
                                weight=FontWeight.W_600,
                            ),
                        ],
                    ),
                ],
            ),
        )

    def __action_row(
        self,
        icon,
        title,
        subtitle,
    ):
        return Row(
            spacing=14,
            controls=[
                Container(
                    width=42,
                    height=42,
                    bgcolor=Colors.GREY_100,
                    border_radius=12,
                    alignment=alignment.center,
                    content=Icon(
                        icon,
                        size=21,
                        color=Colors.GREY_700,
                    ),
                ),
                Column(
                    spacing=2,
                    expand=True,
                    controls=[
                        Text(
                            title,
                            size=14,
                            weight=FontWeight.W_600,
                        ),
                        Text(
                            subtitle,
                            size=12,
                            color=Colors.GREY_600,
                        ),
                    ],
                ),
                Icon(
                    Icons.CHEVRON_RIGHT,
                    size=21,
                    color=Colors.GREY_400,
                ),
            ],
        )
