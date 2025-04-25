# Imports
import flet as ft
from router import Router
from config import db_init_successful


#New Code
INITIAL_ROUTE = "/"  # Default to login

if not db_init_successful:
    INITIAL_ROUTE = "/setup_db"
# New code ends


# Define main function
def main(page: ft.Page):
    app_router = Router(page)
    page.go(INITIAL_ROUTE)

# Run scripts directly
if __name__ == '__main__':
    ft.app(target=main, assets_dir = 'assets')
    
    
