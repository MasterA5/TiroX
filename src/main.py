from flet import (
    Page,
    Row,
    app,
    Text,
    AppBar,
    Container,
    padding,
    Colors,
    Icons,
    NavigationBar,
    NavigationBarDestination,
    SafeArea,
    alignment
)

async def main(page: Page):

    page.appbar = AppBar(
        title=Row(
            controls=[
                Text("TiroX"),
                Container(
                    content=Text("App"),
                    border_radius=20,
                    padding=padding.only(10, 3, 10, 3),
                    bgcolor=Colors.PURPLE
                )
            ],
            spacing=5
        )
    )

    page.navigation_bar = NavigationBar(
        destinations=[
            NavigationBarDestination(label="Home", icon=Icons.HOME),
            NavigationBarDestination(label="Your Data", icon=Icons.FINGERPRINT),
            NavigationBarDestination(label="Settings", icon=Icons.SETTINGS),
        ]
    )

    page.add(
        SafeArea(
            content=Container(
                content=Text("TiroX App", size=50),
                alignment=alignment.center
            ),
            expand=True
        )
    )

app(target=main)