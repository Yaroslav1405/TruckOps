# Imports 
from config import get_supabase_client, reinitialize_supabase
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
        self.setup_routes()
        
    def setup_routes(self):
        current_supabase = get_supabase_client()
        
        self.app_routes = [
            path(url='/', clear=True, view=lambda page, params, basket: LoginPage(current_supabase).view(page, params, basket)),
            path(url='/signup', clear=False, view=lambda page, params, basket: SignupPage(current_supabase).view(page, params, basket)),
            path(url='/setup_db', clear=False, view=lambda page, params, basket: SetupDBPage(self).view(page, params, basket)),
            path(url='/dashboard', clear=True, view=lambda page, params, basket: DispatcherMain(current_supabase, self.page).view(page, params, basket)),
            path(url='/renew', clear=False, view=lambda page, params, basket: RenewCredentials(current_supabase).view(page, params, basket)),
            path(url='/loadsPage', clear=False, view=lambda page, params, basket: MyLoads(current_supabase, self.page).view(page, params, basket)),
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes,
        )
    
    async def reinitialize_routes(self):
        try:
            # Reinitialize the Supabase client
            new_supabase = await reinitialize_supabase()
            if new_supabase:
                self.supabase = get_supabase_client()
                self.setup_routes()
                print("Routes reinitialized with new Supabase client.")
                self.page.go('/')
                return True
            else:
                print("Failed to reinitialize routes due to Supabase client creation failure.")
                return False
        except Exception as e:
            print(f'Error during route reinitialization: {str(e)}')
            return False
