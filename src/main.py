from flet import (
    Locale,
    LocaleConfiguration,
    Page,
    PageTransitionsTheme,
    PageTransitionTheme,
    ScrollMode,
    SliderTheme,
    Theme,
    ThemeMode,
    app,
)
from flet_routing import FletRouter, Params

from core.RegisterManager import RegisterManager
from views.Detail import DetailView
from views.Home import HomeView
from views.NewRegister import NewRegisterView


async def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.AUTO

    page.locale_configuration = LocaleConfiguration(
        supported_locales=[
            Locale("es", "MX"),  # Español (México)
            Locale("en", "US"),  # Inglés (Estados Unidos)
        ],
        current_locale=Locale("es", "MX"),
    )

    manager = RegisterManager()

    page.theme = Theme(
        page_transitions=PageTransitionsTheme(
            windows=PageTransitionTheme.CUPERTINO,
            android=PageTransitionTheme.CUPERTINO,
            linux=PageTransitionTheme.CUPERTINO,
            ios=PageTransitionTheme.CUPERTINO,
            macos=PageTransitionTheme.CUPERTINO,
        ),
        slider_theme=SliderTheme(track_height=12),
    )

    router = FletRouter(page=page, initial_route="/")

    @router.route("/")
    def home(params: Params):
        return HomeView(params, manager)

    @router.route("/create/register")
    def new_register(params: Params):
        return NewRegisterView(params, manager)

    @router.route("/detail/:id")
    def detail(params: Params):
        return DetailView(params, manager)


app(target=main)
