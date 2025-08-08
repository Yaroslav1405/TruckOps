# Imports 
import flet as ft
from flet_route import Routing, path
from pages.login import LoginPage
from pages.signup import SignupPage
from pages.dashboard import DispatcherMain
from pages.renew import RenewCredentials
from pages.loads import MyLoads
from pages.setup_db import SetupDBPage

class Router:
    def __init__(self, page: ft.Page, supabase):
        self.page = page
        self.supabase = supabase
        self.app_routes = [
            path(url='/', clear=True, view=lambda page, params, basket: LoginPage(self.supabase).view(page, params, basket)),
            path(url='/signup', clear=False, view=lambda page, params, basket: SignupPage(self.supabase).view(page, params, basket)),
            path(url='/setup_db', clear=False, view=lambda page, params, basket: SetupDBPage().view(page, params, basket)),
            path(url='/dashboard', clear=True, view=lambda page, params, basket: DispatcherMain(self.supabase, self.page).view(page, params, basket)),
            path(url='/renew', clear=False, view=lambda page, params, basket: RenewCredentials(self.supabase).view(page, params, basket)),
            path(url='/loadsPage', clear=False, view=lambda page, params, basket: MyLoads(self.supabase, self.page).view(page, params, basket)),
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes,
        )
