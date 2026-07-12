from uuid import UUID

from flet import (
    AppBar,
    Colors,
    Column,
    Container,
    FontWeight,
    IconButton,
    Icons,
    MainAxisAlignment,
    Row,
    Text,
    View,
    border,
)
from flet_routing import Params

from components.DetailCard import DetailCard
from components.RangeCard import RangeCard
from components.StylishButton import StylishButton
from components.StylishDialog import QRSuccessfullyCreated
from core.RegisterManager import RegisterManager
from utils.formater import Formater
from utils.generate_qrcode import generate_qrcode


class DetailView(View):
    def __init__(self, params: Params, manager: RegisterManager | None = None):
        super().__init__(f"/detail/{params.path['id']}")
        self.params = params
        self.router = self.params.router
        self.scroll = "auto"
        self.register_manager = manager
        self.data = self.get_register_info()
        self.appbar = AppBar(
            title=Text(f"{Formater.format_datetime(str(self.data.date))[0]}"),
            leading=IconButton(
                icon=Icons.ARROW_BACK,
                on_click=lambda e: self.router.replace(
                    "/", {"lst_idx": self.params.private.get("lst_idx", 1)}
                ),
            ),
        )
        self.controls = [
            DetailCard(
                value=float(self.data.value),
                date=Formater.format_datetime(str(self.data.date), legible=True),
            ),
            RangeCard(self.data.value),
            Container(
                content=Column(
                    controls=[
                        Text("Notas", weight=FontWeight.W_800),
                        Row(
                            controls=[
                                Container(
                                    content=Text(
                                        "No Hay Notas En Este Registro"
                                        if not self.data.notes
                                        else self.data.notes,
                                        weight=FontWeight.W_800,
                                    ),
                                    padding=10,
                                    border=border.all(3, Colors.GREY_300),
                                    border_radius=20,
                                    expand=True,
                                    height=200,
                                ),
                            ],
                            expand=True,
                        ),
                    ]
                )
            ),
            Row(
                controls=[
                    StylishButton(
                        text="Generar Codigo QR Del Registro",
                        icon=Icons.QR_CODE,
                        bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                        on_click=self.generate_code,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            Row(
                controls=[
                    StylishButton(
                        text="Eliminar Registro",
                        icon=Icons.DELETE,
                        bgcolor=Colors.DEEP_PURPLE_ACCENT_200,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
        ]

    def get_register_info(self):
        reg_id = UUID(self.params.path.get("id"))
        register = self.register_manager.get_register_data_by_id(reg_id)
        return register

    def generate_code(self, e):
        image_base64 = generate_qrcode(self.data)

        self.page.open(QRSuccessfullyCreated(image_base64))
