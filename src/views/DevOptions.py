import asyncio
import os
from pathlib import Path

from flet import (
    AlertDialog,
    AppBar,
    Colors,
    Container,
    ControlEvent,
    IconButton,
    Icons,
    MainAxisAlignment,
    OptionalControlEventCallable,
    ProgressRing,
    Row,
    Text,
    TextField,
    View,
    alignment,
)
from flet_routing import FletRouter, Params

from components.StylishButton import StylishButton
from components.StylishDialog import StylishDialog


def change_url(e: ControlEvent):
    try:
        path = Path(os.getcwd(), "src", ".env")

        with open(path, "r") as f:
            lines = f.readlines()

        with open(path, "w") as f:
            for line in lines:
                if line.strip().startswith("# TIROX_SERVER_URL="):
                    line = line.replace("# TIROX_SERVER_URL=", "TIROX_SERVER_URL=", 1)

                if line.strip().startswith(
                    "TIROX_SERVER_URL="
                ) or line.strip().startswith("TIROX_SERVER_URL = "):
                    line = f"TIROX_SERVER_URL = {e.control.value.strip()}\n"

                f.write(line)

    except FileNotFoundError:
        pass


class DevOptionView(View):
    def __init__(
        self,
        params: Params,
        on_change_url: OptionalControlEventCallable = None,
    ):
        super().__init__("/dev-options")
        self.params = params
        self.on_change_url = on_change_url
        self.router: FletRouter = self.params.router
        self.appbar = AppBar(
            title=Text("Dev Options"),
            center_title=True,
            leading=IconButton(
                icon=Icons.ARROW_BACK,
                on_click=lambda e: self.router.replace(
                    "/",
                    {"lst_idx": self.params.private.get("lst_idx", 2)},
                ),
            ),
        )
        self.controls = [
            Container(
                content=TextField(
                    label="Url Del Servidor",
                    value=os.getenv("TIROX_SERVER_URL"),
                    border_radius=20,
                    border_color=Colors.DEEP_PURPLE_ACCENT_200,
                    on_submit=self.__handle_url_change,
                ),
                border_radius=20,
                padding=10,
            ),
            Container(
                content=StylishButton(
                    "Aplicar Cambios",
                    on_click=lambda e: self.router.replace(
                        "/",
                        {"lst_idx": self.params.private.get("lst_idx", 2)},
                    ),
                ),
            ),
        ]

    async def __handle_url_change(self, e):
        if not self.page:
            return

        dialog = AlertDialog(
            content=Row(
                controls=[
                    Container(
                        content=ProgressRing(),
                        bgcolor=Colors.TRANSPARENT
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            bgcolor=Colors.TRANSPARENT
        )

        change_url(e)
        self.page.open(dialog)
        await asyncio.sleep(1)
        self.page.close(dialog)
