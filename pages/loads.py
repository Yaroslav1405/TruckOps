from db.requests import fetch_loads
import flet as ft
from flet_route import Params, Basket
import datetime
from helper_functions import NewLoad, show_message, create_snackbar, create_logo, create_sidebar, create_header
from assets.styles import *
from storage.session import SessionManager

class MyLoads:
    def __init__(self, supabase, page):
        self.supabase = supabase
        self.selected_date = datetime.date.today()
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)
        self.page = page
        user_data = SessionManager.get_user_data(page)
        self.user_id = user_data.get('user_id')
        self.access_token = user_data.get('access_token')
    
    # Define Table Display 
    async def _populate_table(self, page: ft.Page):
        self.supabase.postgrest.auth(self.access_token) # Can we move this somewhere else? 
        loads = await fetch_loads(user_id=self.user_id, page=page,error_snackbar=self.error_snackbar)
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
                                on_click=lambda e, load_id = load_id: self.delete_alert_dialog(load_id, page),
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
    
        
    # Define Alert Dialog for load deletion
    def delete_alert_dialog(self, load_id, page):
        # Handle Deletion
        async def handle_delete(e):
            try:
                if hasattr(self, 'current_loads_table'):
                    await self.supabase.table('Loads').delete().eq('id', load_id).execute()
                    page.close(dialog)
                    rows = await self._populate_table(page)
                    self.current_loads_table.rows = rows
                    page.update()
                    # await self._refresh_table()
                    print('Page updated with new data after deletion')
                    show_message(page, self.success_snackbar, 'Load was deleted successfully')
                
            except Exception as ex:
                print(f"Error deleting load: {ex}")
                show_message(page, self.error_snackbar, 'Error deleting a load! Please try again later.')
            
        # Handle Dismissal
        def cancel_delete(e):
            page.close(dialog)

        # Define Alert Dialog
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm", font_family = 'lato-regular'),
            content=ft.Text("Are you sure you want to delete this file?", font_family = 'lato-regular', size = buttonFontSize),
            actions=[
                ft.TextButton("Yes", on_click=handle_delete),
                ft.TextButton("No", on_click=cancel_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.open(dialog)
    
    # Create Lodas Table (Not populated)
    def _create_loads_table(self, page: ft.Page):
        # Define Table for Existing Loads
        return ft.DataTable(
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
            rows=[]
        )

                    
    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        # Set page parameters
        page.window.min_height = minWindowHeight
        page.window.min_width = minWindowWidth

        page.title = 'TruckOps - My Loads'
        page.fonts = {'lato-bold': 'assets/Lato-Bold.ttf', 'lato-regular': 'assets/Lato-Regular.ttf',
                      'lato-light': 'assets/Lato-Light.ttf'}
        if not SessionManager.require_auth(page):
            return ft.View('/loads', bgcolor=defaultBackgroundColor, controls=[ft.Text("Redirecting to login...")])
        
        loads_table = self._create_loads_table(page)
        self.current_loads_table = loads_table
        
        async def load_data():
            rows = await self._populate_table(page)
            loads_table.rows = rows
            page.update()
            print('Page updated with new data')
            
        page.run_task(load_data)
        
        # load_dialog = NewLoad(page, self.refresh_table)
        load_dialog = NewLoad(page, load_data)
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
                                            create_header('Loads', load_dialog.get_handler()),
                                            # create_header('Loads', self.new_load),
                                            ft.Divider(),
                                            ft.Container(
                                                content = loads_table,
                                                padding = ft.padding.all(10)),
                                        ],
                                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    ),
                        )
                    ]
                )
            ] 
        )