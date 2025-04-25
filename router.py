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
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url='/', clear=True, view=LoginPage().view),
            path(url='/signup', clear=False, view=SignupPage().view),
            path(url='/setup_db', clear=False, view=SetupDBPage().view),
            path(url='/dashboard', clear=True, view=DispatcherMain().view),
            path(url='/renew', clear=False, view=RenewCredentials().view),
            path(url='/loadsPage', clear=False, view=MyLoads().view),
            
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes,
        )
        #self.page.go(self.page.route)