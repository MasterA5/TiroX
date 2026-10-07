import os

from flet import (
    Locale,
    LocaleConfiguration,
    Page,
    PagePlatform,
    PageTransitionsTheme,
    PageTransitionTheme,
    ScrollMode,
    SliderTheme,
    Theme,
    ThemeMode,
    app,
)
from flet_routing import FletRouter, Params

from core.AuthManager import TiroxAuthManager
from core.RegisterManager import RegisterManager
from views.About import AboutView
from views.AccountView import AccountView
from views.Detail import DetailView
from views.DevOptions import DevOptionView
from views.Home import HomeView
from views.Login import LoginView
from views.NewRegister import NewRegisterView
from views.Notification import NotificationsView
from views.Register import RegisterView


def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.AUTO

    if page.platform == PagePlatform.WINDOWS:
        page.window.width = 500
        page.window.height = 900
        page.window.resizable = False
        page.window.maximizable = False

    page.locale_configuration = LocaleConfiguration(
        supported_locales=[
            Locale("es", "MX"),  # Español (México)
            Locale("en", "US"),  # Inglés (Estados Unidos)
        ],
        current_locale=Locale("es", "MX"),
    )

    auth_manager = TiroxAuthManager()
    manager = RegisterManager(auth_manager)

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

    router = FletRouter(
        page=page,
        initial_route="/",
        not_auth_redirect_route="/login",
        auth_checker=lambda: auth_manager.is_auth(),
    )

    @router.route("/login")
    def login(params: Params):
        return LoginView(params, auth_manager)

    @router.route("/", protected=True)
    def home(params: Params):
        return HomeView(params, manager)

    @router.route("/create/register")
    def new_register(params: Params):
        return NewRegisterView(params, manager)

    @router.route("/detail/:id")
    def detail(params: Params):
        return DetailView(params, manager)

    @router.route("/account")
    def account(params: Params):
        return AccountView(params, auth_manager)

    @router.route("/about")
    def about(params: Params):
        return AboutView(params)

    @router.route("/notifications")
    def notifications(params: Params):
        return NotificationsView(params)

    @router.route("/register")
    def register_view(params: Params):
        return RegisterView(params, auth_manager)

    if os.getenv("BUILD_STATE", "production") == "dev":
        @router.route("/dev-options")
        def dev_options(params: Params):
            return DevOptionView(params)

app(target=main)
