import random

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
)
from flet_routing import Params

from components.DetailCard import DetailCard
from components.RangeCard import RangeCard


class DetailView(View):
    def __init__(self, params: Params):
        super().__init__(f"/detail/{params.path['id']}")
        self.params = params
        self.router = self.params.router
        self.scroll = "auto"
        self.appbar = AppBar(
            title=Text("Details"),
            leading=IconButton(
                icon=Icons.ARROW_BACK,
                on_click=lambda e: self.router.replace(
                    "/"
                ),
            ),
        )
        self.controls = [
            DetailCard(
                value=float(f"{random.uniform(1, 9):.2f}"),
                date="20 may 2024 - 8:50 AM"
            ),
            RangeCard(),
            Container(
                content=Column(
                    controls=[
                        Text("Notas", weight=FontWeight.W_800),
                        Text("Sin Notas", weight=FontWeight.W_300),
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
                        bgcolor=Colors.WHITE
                    ),
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ]
