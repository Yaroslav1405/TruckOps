# Imports
import flet as ft
from router import Router
from config import create_supabase, get_supabase_client
from storage.session import SessionManager
import logging
import betterlogging as bl


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting application...')
    
# Define main function
async def main(page: ft.Page):
    setup_logging()
    await create_supabase()
    supabase = get_supabase_client()
    active_session = SessionManager.retrieve_session_data(page)
    if not supabase:
        route = "/setup_db"
    elif active_session:
        route = "/dashboard"
    else: route = '/'
    app_router = Router(page, supabase)
    page.go(route)

# Run scripts directly
if __name__ == '__main__':
    ft.app(target=main, assets_dir = 'assets')
    