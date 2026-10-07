from flet import (
    AppBar,
    BoxShadow,
    ButtonStyle,
    Colors,
    Column,
    Container,
    ControlEvent,
    CrossAxisAlignment,
    FontWeight,
    Icons,
    Image,
    ImageFit,
    InputBorder,
    MainAxisAlignment,
    Offset,
    Row,
    ScrollMode,
    Text,
    TextAlign,
    TextButton,
    TextField,
    TextSpan,
    TextStyle,
    View,
    padding,
)
from flet_routing import Params

from components.StylishButton import StylishButton
from components.StylishSnackBar import ErrorSnackBar
from core.AuthManager import TiroxAuthManager


class LoginView(View):
    def __init__(self, params: Params, auth_manager: TiroxAuthManager | None = None):
        super().__init__("/login")
        self.params = params
        self.auth_manager = auth_manager
        self.email_field = TextField(
            label="Email",
            hint_text="Enter your email",
            prefix_icon=Icons.EMAIL_OUTLINED,
            border=InputBorder.OUTLINE,
            border_radius=12,
            filled=True,
            fill_color=Colors.WHITE,
            border_color=Colors.GREY_300,
            focused_border_color=Colors.DEEP_PURPLE_ACCENT_200,
            cursor_color=Colors.DEEP_PURPLE_ACCENT_200,
            label_style=TextStyle(color=Colors.GREY_700),
            text_style=TextStyle(color=Colors.BLACK87),
            content_padding=padding.symmetric(horizontal=16, vertical=16),
        )
        self.password_field = TextField(
            label="Password",
            hint_text="Enter your password",
            prefix_icon=Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            border=InputBorder.OUTLINE,
            border_radius=12,
            filled=True,
            fill_color=Colors.WHITE,
            border_color=Colors.GREY_300,
            focused_border_color=Colors.DEEP_PURPLE_ACCENT_200,
            cursor_color=Colors.DEEP_PURPLE_ACCENT_200,
            label_style=TextStyle(color=Colors.GREY_700),
            text_style=TextStyle(color=Colors.BLACK87),
            content_padding=padding.symmetric(horizontal=16, vertical=16),
        )
        self.appbar = AppBar(
            title=Text(
                "Tiro",
                size=30,
                weight=FontWeight.BOLD,
                spans=[
                    TextSpan(
                        "X",
                        style=TextStyle(
                            color=Colors.DEEP_PURPLE_ACCENT_200,
                        ),
                    ),
                ],
            ),
            center_title=True,
            bgcolor=Colors.TRANSPARENT,
            elevation=0,
        )
        logo = Container(
            content=Image(
                "/icon.png",
                width=105,
                height=105,
                fit=ImageFit.CONTAIN,
            ),
            width=125,
            height=125,
            padding=10,
            border_radius=30,
            bgcolor=Colors.WHITE,
            shadow=BoxShadow(
                blur_radius=25,
                spread_radius=1,
                color=Colors.BLACK12,
                offset=Offset(0, 8),
            ),
        )
        title = Row(
            controls=[
                Text(
                    "Inicio De Sesión ",
                    size=34,
                    weight=FontWeight.BOLD,
                    color=Colors.BLACK87,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=0,
        )

        subtitle = Text(
            "Bienvenido De Vuelta ☺",
            size=14,
            color=Colors.GREY_600,
            text_align=TextAlign.CENTER,
        )
        login_card = Container(
            content=Column(
                controls=[
                    Text(
                        "Sign in",
                        size=22,
                        weight=FontWeight.BOLD,
                        color=Colors.BLACK87,
                    ),
                    Text(
                        "Enter your credentials below",
                        size=13,
                        color=Colors.GREY_600,
                    ),
                    Container(height=8),
                    self.email_field,
                    self.password_field,
                    Container(height=4),
                    StylishButton(
                        "Login",
                        on_click=lambda e: self.page.run_task(self.__login, e),
                    ),
                    TextButton(
                        text="No Tienes Cuenta? Crea una Aqui",
                        style=ButtonStyle(
                            color=Colors.DEEP_PURPLE_ACCENT_200,
                            text_style=TextStyle(color=Colors.DEEP_PURPLE_ACCENT_200),
                            overlay_color=Colors.TRANSPARENT
                        ),
                        on_click=lambda e: self.params.router.push("/register")
                    ),
                ],
                spacing=14,
                horizontal_alignment=CrossAxisAlignment.STRETCH,
            ),
            width=430,
            padding=padding.all(28),
            bgcolor=Colors.WHITE,
            border_radius=24,
            shadow=BoxShadow(
                blur_radius=35,
                spread_radius=2,
                color=Colors.BLACK12,
                offset=Offset(0, 12),
            ),
        )
        self.controls = [
            Container(
                expand=True,
                padding=padding.symmetric(
                    horizontal=20,
                    vertical=35,
                ),
                bgcolor=Colors.GREY_50,
                content=Column(
                    controls=[
                        logo,
                        Container(height=18),
                        title,
                        Container(height=4),
                        subtitle,
                        Container(height=25),
                        login_card,
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    alignment=MainAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                ),
            )
        ]

    async def __login(self, e: ControlEvent):
        email = (self.email_field.value or "").strip()
        password = self.password_field.value or ""

        if not email or not password:
            self.page.open(ErrorSnackBar("Completa todos los campos"))
            return

        session = await self.auth_manager.login(email=email, password=password)

        if session:
            self.params.router.replace("/")
        else:
            self.page.open(
                ErrorSnackBar("Credenciales incorrectas o sin conexión al servidor")
            )

        return
