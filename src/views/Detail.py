from uuid import UUID

from flet import (
    AppBar,
    Button,
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
from core.RegisterManager import RegisterManager
from utils.formater import Formater


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
                                    height=300,
                                ),
                            ],
                            expand=True,
                        ),
                    ]
                )
            ),
            Row(
                controls=[
                    Button(
                        text="Eliminar Registro",
                        icon=Icons.DELETE,
                        icon_color=Colors.RED,
                        color=Colors.RED,
                        bgcolor=Colors.WHITE,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
        ]

    def get_register_info(self):
        reg_id = UUID(self.params.path.get("id"))
        register = self.register_manager.get_register_data_by_id(reg_id)
        return register
