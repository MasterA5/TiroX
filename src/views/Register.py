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
    KeyboardType,
    MainAxisAlignment,
    MouseCursor,
    Offset,
    Row,
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


class RegisterView(View):
    def __init__(self, params: Params, auth_manager: TiroxAuthManager | None = None):
        super().__init__("/register", scroll="auto")
        self.params = params
        self.auth_manager = auth_manager

        self.username_field = TextField(
            label="Nombre De Usuario",
            hint_text="Escribe Tu Nombre De Usuario",
            prefix_icon=Icons.PERSON_OUTLINE,
            border=InputBorder.OUTLINE,
            border_radius=12,
            filled=True,
            fill_color=Colors.WHITE,
            border_color=Colors.GREY_300,
            focused_border_color=Colors.DEEP_PURPLE_ACCENT_200,
            cursor_color=Colors.DEEP_PURPLE_ACCENT_200,
            label_style=TextStyle(color=Colors.GREY_700),
            text_style=TextStyle(color=Colors.BLACK87),
            content_padding=padding.symmetric(
                horizontal=16,
                vertical=16,
            ),
        )

        self.email_field = TextField(
            label="Email",
            hint_text="Escribe Tu email",
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
            content_padding=padding.symmetric(
                horizontal=16,
                vertical=16,
            ),
        )

        self.password_field = TextField(
            label="Contraseña",
            hint_text="Escribe Tu Contraseña",
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
            content_padding=padding.symmetric(
                horizontal=16,
                vertical=16,
            ),
        )

        self.confirm_password_field = TextField(
            label="Confirmar Contraseña",
            hint_text="Repite Tu Contraseña",
            prefix_icon=Icons.LOCK_RESET_OUTLINED,
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
            content_padding=padding.symmetric(
                horizontal=16,
                vertical=16,
            ),
        )

        self.first_name_field = TextField(
            label="Primer Nombre",
            hint_text="Escribe Tu Primer Nombre",
            prefix_icon=Icons.PERSON,
            border=InputBorder.OUTLINE,
            border_radius=12,
            filled=True,
            fill_color=Colors.WHITE,
            border_color=Colors.GREY_300,
            focused_border_color=Colors.DEEP_PURPLE_ACCENT_200,
            cursor_color=Colors.DEEP_PURPLE_ACCENT_200,
            label_style=TextStyle(color=Colors.GREY_700),
            text_style=TextStyle(color=Colors.BLACK87),
            content_padding=padding.symmetric(
                horizontal=16,
                vertical=16,
            ),
        )

        self.last_name_field = TextField(
            label="Apellido",
            hint_text="Escribe Tu Apellido",
            prefix_icon=Icons.PERSON,
            border=InputBorder.OUTLINE,
            border_radius=12,
            filled=True,
            fill_color=Colors.WHITE,
            border_color=Colors.GREY_300,
            focused_border_color=Colors.DEEP_PURPLE_ACCENT_200,
            cursor_color=Colors.DEEP_PURPLE_ACCENT_200,
            label_style=TextStyle(color=Colors.GREY_700),
            text_style=TextStyle(color=Colors.BLACK87),
            content_padding=padding.symmetric(
                horizontal=16,
                vertical=16,
            ),
        )

        self.age_field = TextField(
            label="Edad",
            hint_text="Escribe Tu Edad",
            prefix_icon=Icons.NUMBERS,
            border=InputBorder.OUTLINE,
            border_radius=12,
            filled=True,
            fill_color=Colors.WHITE,
            border_color=Colors.GREY_300,
            focused_border_color=Colors.DEEP_PURPLE_ACCENT_200,
            cursor_color=Colors.DEEP_PURPLE_ACCENT_200,
            label_style=TextStyle(color=Colors.GREY_700),
            text_style=TextStyle(color=Colors.BLACK87),
            content_padding=padding.symmetric(
                horizontal=16,
                vertical=16,
            ),
            keyboard_type=KeyboardType.NUMBER,
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
                width=90,
                height=90,
                fit=ImageFit.CONTAIN,
            ),
            width=110,
            height=110,
            padding=10,
            border_radius=28,
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
                    "Creacion De Cuenta",
                    size=34,
                    weight=FontWeight.BOLD,
                    color=Colors.BLACK87,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=0,
        )

        subtitle = Text(
            "Crea Tu Cuenta Para Poder Continuar.",
            size=14,
            color=Colors.GREY_600,
            text_align=TextAlign.CENTER,
        )

        register_card = Container(
            content=Column(
                controls=[
                    Text(
                        "Crea Tu Cuenta",
                        size=22,
                        weight=FontWeight.BOLD,
                        color=Colors.BLACK87,
                    ),
                    Text(
                        "Completa Los Campos A Continuacion",
                        size=13,
                        color=Colors.GREY_600,
                    ),
                    self.username_field,
                    self.email_field,
                    self.first_name_field,
                    self.last_name_field,
                    self.age_field,
                    self.password_field,
                    self.confirm_password_field,
                    Container(height=4),
                    StylishButton(
                        "Crear Cuenta",
                        on_click=lambda e: self.page.run_task(
                            self.__register,
                            e,
                        ),
                    ),
                    TextButton(
                        text="Ya Tienes Cuenta? Inicia Sesión una Aqui",
                        style=ButtonStyle(
                            color=Colors.DEEP_PURPLE_ACCENT_200,
                            text_style=TextStyle(color=Colors.DEEP_PURPLE_ACCENT_200),
                            overlay_color=Colors.TRANSPARENT,
                            mouse_cursor=MouseCursor.CLICK,
                        ),
                        on_click=lambda e: self.params.router.replace("/login"),
                    ),
                ],
                spacing=12,
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
                    vertical=30,
                ),
                bgcolor=Colors.GREY_50,
                content=Column(
                    controls=[
                        logo,
                        title,
                        Container(height=4),
                        subtitle,
                        Container(height=22),
                        register_card,
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    alignment=MainAxisAlignment.CENTER,
                ),
            )
        ]

    async def __register(self, e: ControlEvent):
        values = {
            "username": (self.username_field.value or "").strip(),
            "email": (self.email_field.value or "").strip(),
            "first_name": (self.first_name_field.value or "").strip(),
            "last_name": (self.last_name_field.value or "").strip(),
            "age": (self.age_field.value or "").strip(),
            "password": self.password_field.value or "",
            "confirm_password": self.confirm_password_field.value or "",
        }

        if not all(values.values()):
            self.page.open(ErrorSnackBar("Completa todos los campos"))
            return

        if (
            "@" not in values["email"]
            or "." not in values["email"].split("@")[-1]
        ):
            self.page.open(ErrorSnackBar("Ingresa un email válido"))
            return

        if values["password"] != values["confirm_password"]:
            self.page.open(ErrorSnackBar("Las contraseñas no coinciden"))
            return

        try:
            age = int(values["age"])
            if age <= 0:
                raise ValueError
        except ValueError:
            self.page.open(ErrorSnackBar("La edad debe ser un número válido"))
            return

        session = await self.auth_manager.register(
            username=values["username"],
            email=values["email"],
            password=values["password"],
            first_name=values["first_name"],
            last_name=values["last_name"],
            age=age,
        )

        if session:
            self.params.router.replace("/")
        else:
            self.page.open(
                ErrorSnackBar(
                    "No se pudo crear la cuenta (usuario/email en uso o sin conexión)"
                )
            )

        return
