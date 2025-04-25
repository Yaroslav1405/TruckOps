# Imports
import flet as ft
from flet_route import Params, Basket
from config import supabase
import datetime
from helper_functions import show_message, create_snackbar, create_logo, create_sidebar, add_load, create_header
from assets.styles import *

class MyLoads:
    def __init__(self):
        self.supabase = supabase
        self.user_id = None
        self.selected_date = datetime.date.today()
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)
    
    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        
        # Set page parameters
        page.window.min_height = minWindowHeight
        page.window.min_width = minWindowWidth
        page.title = 'TruckOps - My Loads'
        page.fonts = {'lato-bold': 'assets/Lato-Bold.ttf', 'lato-regular': 'assets/Lato-Regular.ttf',
                      'lato-light': 'assets/Lato-Light.ttf'}
        
        # Retrieve Values from Client Storage
        self.user_id = page.client_storage.get('user_id')
        access_token = page.client_storage.get('access_token')
        refresh_token = page.client_storage.get('refresh_token')
        
        # Log out User if not Logged in
        if not access_token or not refresh_token or not self.user_id:
            show_message(page, self.error_snackbar, "Session expired. Please log in again.")
            page.go('/')
            return
        
        # Set the Session
        self.supabase.auth.set_session(access_token, refresh_token)
        self.supabase.postgrest.auth(access_token)
        
        
        # Define Load Fetching from Database
        def fetch_loads():
            try:
                response = self.supabase.table("Loads").select("*").eq("dispatcher_name", self.user_id).order('date', desc=True).limit(10).execute()
                loads_data = response.data
                return loads_data
            except Exception as e:
                show_message(page, self.error_snackbar, f'Fetch error: {e}')
                return []
        
        
        # Define Table Display 
        def populate_table():
            loads = fetch_loads()
            rows = []
            # Loop through loads
            for load in loads:
                load_id = load.get('id')
                # Insert load into the table
                rows.append(
                    ft.DataRow(
                        cells = [
                            ft.DataCell(ft.Text(str(load['date']), font_family = 'lato-light')),
                            ft.DataCell(ft.Text(load['company_name'], font_family = 'lato-light')),
                            ft.DataCell(ft.Text(load['driver_name'], font_family = 'lato-light')),
                            ft.DataCell(ft.Text(load['origin'], font_family = 'lato-light')),
                            ft.DataCell(ft.Text(load['destination'], font_family = 'lato-light')),
                            ft.DataCell(ft.Text(str(load['miles_driven']), font_family = 'lato-light')),
                            ft.DataCell(ft.Text(str(load['deadhead']), font_family = 'lato-light')),
                            ft.DataCell(ft.Text(str(load['total_miles']), font_family = 'lato-light')),
                            ft.DataCell(ft.Text(load['total_rate'], font_family = 'lato-light')),
                            ft.DataCell(ft.Text(f"{load['rate_per_mile']:.2f}", font_family = 'lato-light')),
                            ft.DataCell(
                                ft.ElevatedButton(
                                    "Delete",
                                    on_click=lambda e, load_id = load_id: delete_alert_dialog(load_id),
                                    icon = ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_color = defaultFontColor,
                                    bgcolor=defaultRedButtonColor,
                                    color=defaultFontColor,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        text_style=ft.TextStyle(
                                            size=buttonFontSize,
                                            font_family='lato-regular',
                                        )
                                    )
                                    
                                )
                            ),
                        ]
                    )
                )
            return rows
        
        
        # Define Alert Dialog for Load Deletion
        def delete_alert_dialog(load_id):
            
            # Handle Deletion
            def handle_delete(e):
                try:
                    self.supabase.postgrest.auth(access_token)
                    self.supabase.table('Loads').delete().eq('id', load_id).execute()
                    existing_loads.rows = populate_table()
                    existing_loads.update()
                    page.close(dialog)
                    show_message(page, self.success_snackbar, 'Load was deleted successfully')
                except Exception as ex:
                    show_message(page, self.error_snackbar, f'Error deleting a load: {ex}')
            
            
            # Handle Dismissal
            def handle_close(e):
                page.close(dialog)

            # Define Alert Dialog
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm", font_family = 'lato-regular'),
                content=ft.Text("Are you sure you want to delete this file?", font_family = 'lato-regular', size = buttonFontSize),
                actions=[
                    ft.TextButton("Yes", on_click=handle_delete),
                    ft.TextButton("No", on_click=handle_close),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.open(dialog)
        
        
            
        # Define Table for Existing Loads
        existing_loads = ft.DataTable(
            sort_column_index=0,
            sort_ascending=True,
            columns=[
                ft.DataColumn(ft.Text('Date', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Company Name', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Driver Name', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Origin', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Destination', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Miles Driven', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Deadhead', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Total Miles', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Total Rate', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Rate per Mile', font_family = 'lato-bold', size = buttonFontSize)),
                ft.DataColumn(ft.Text('Actions', font_family = 'lato-bold', size = buttonFontSize)),
            ],
            rows=populate_table()
        )


        # Define Refresh Function for Existing Loads
        def refresh_loads():
            existing_loads.rows = populate_table()
            existing_loads.update()
            page.update()

        # Define New Load
        def new_load(e):
            show_form = add_load(self, page, refresh_callback=refresh_loads)
            show_form(e)

        
        return ft.View(
            '/loadsPage',
            bgcolor = defaultBackgroundColor,
            padding = ft.padding.all(15),
            controls = [
                ft.Row(
                    expand = True,
                    controls = [
                        # Sidebar
                        ft.Container(
                            expand = 1,
                            content = ft.Column(
                                controls = [
                                    # Logo Container
                                    ft.Container(
                                        content = create_logo(140, 80),
                                        alignment = ft.alignment.center,
                                        width=200
                                    ),
                                    create_sidebar(page, font_family = 'lato-light')
                                ],
                            )
                        ),
                        # Divider
                        ft.VerticalDivider(width=1),
                        # Main Content Buttons  
                        ft.Container(
                            expand = 9,
                            content = ft.Column(
                                        controls = [
                                            create_header('Loads', new_load),
                                            ft.Divider(),
                                            ft.Container(
                                                content = existing_loads,
                                                padding = ft.padding.all(10)),
                                        ],
                                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    ),
                        )
                    ]
                )
            ]
        )