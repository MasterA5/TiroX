from flet import (
    Page,
    PageTransitionsTheme,
    PageTransitionTheme,
    ScrollMode,
    SliderTheme,
    Text,
    Theme,
    ThemeMode,
    View,
    app,
)
from flet_routing import FletRouter, Params

from views.Home import HomeView
from views.NewRegister import NewRegisterView


async def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.AUTO

    page.theme = Theme(
        page_transitions=PageTransitionsTheme(
            windows=PageTransitionTheme.CUPERTINO,
            android=PageTransitionTheme.CUPERTINO,
            linux=PageTransitionTheme.FADE_UPWARDS,
            ios=PageTransitionTheme.CUPERTINO,
            macos=PageTransitionTheme.CUPERTINO
        ),
        slider_theme=SliderTheme(
            track_height=30
        )
    )

    router = FletRouter(page=page, initial_route="/")

    @router.route("/")
    def home(params: Params):
        return HomeView(params)

    @router.route("/create/register")
    def new_register(params: Params):
        return NewRegisterView(params)

    @router.route("/test")
    def test(params: Params):
        return View("/test", controls=[Text("This is a test")])

    # router.push("/create/register")

app(target=main)
