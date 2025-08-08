# Imports
from config import get_supabase_client
import flet as ft
import re
import requests
import datetime
from assets.styles import *
from storage.session import SessionManager

# Define Logo function
def create_logo(width: int, height: int) -> ft.Container:
    """Creates a logo Container."""
    return ft.Container(
        content=ft.Image(
            src='images/logo.png',
            width=width,
            height=height,
            fit=ft.ImageFit.FILL
        ),
        alignment=ft.alignment.center,
        expand=False,
    )


# Define Snackbar function
def create_snackbar(background_color) -> ft.SnackBar:
    """Creates a standard error Snackbar."""
    return ft.SnackBar(
        content = ft.Text(
            value = "",
            color = ft.Colors.WHITE,
            size = 16,
            font_family = 'lato-light'
        ),
        bgcolor = background_color,
        action = 'Dismiss',
        duration = 3000
    )


# Show snackbar message function
def show_message(page: ft.Page, snackbar: ft.SnackBar, message: str):
    """Displays an error message using a Flet SnackBar."""
    snackbar.content.value = message
    page.open(snackbar)


# Email validation function
def validate_email(email: str) -> bool:
    """Simple email validation."""
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None


# Define Sidebar function 
def create_sidebar(page: ft.Page, font_family: str = None) -> ft.Container:
    """Creates a sidebar Container."""
    
    # Text Styles 
    text_style = {'size': 18, 'color': defaultFontColor}
    
    # Font 
    if font_family:
        text_style['font_family'] = font_family
    
    def handle_logout():
        async def logout():
            await SessionManager.logout(page, get_supabase_client())
            print('Called logout function')
        page.run_task(logout)
        
        
    return ft.Container(
        padding = 10,
        content=ft.Column(
            controls=[
                # Buttons
                ft.Column(
                    controls = [
                        ft.Text('Menu',**text_style),
                        ft.TextButton(
                            'Dashboard',
                            on_click=lambda _: page.go('/dashboard'),
                            icon=ft.Icons.HOME_OUTLINED,
                            style=ft.ButtonStyle(text_style=ft.TextStyle(**text_style), color=text_style['color'])
                        ),
                        ft.Container(height=10),
                        ft.Text('Operations', **text_style),
                        ft.TextButton(
                            'Loads',
                            on_click=lambda _: page.go('/loadsPage'),
                            icon=ft.Icons.LOCAL_SHIPPING_OUTLINED,
                            style=ft.ButtonStyle(text_style=ft.TextStyle(**text_style), color=text_style['color'])
                        ),
                        ft.TextButton(
                            'Chat',
                            icon=ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED,
                            style=ft.ButtonStyle(text_style=ft.TextStyle(**text_style), color=text_style['color'])
                        )
                    ],
                    spacing = 15
                ),
                # Spacer
                ft.Container(expand=True),
                # Logout
                ft.Container(
                    content=ft.ElevatedButton(
                        "Logout",
                        on_click=lambda _: handle_logout(),
                        height = 40,
                        width=200,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            bgcolor=defaultRedButtonColor,
                            color = defaultFontColor,
                            text_style=ft.TextStyle(
                                size=20,
                                font_family = 'lato-regular',
                            ),
                        ),
                    ),
                    alignment=ft.alignment.bottom_center,
                ),
            ],
            expand=True,
        ),
        expand=True,
    )           
    

# Define Header Function
def create_header(title: str, add_load_function: callable) -> ft.Container:
    return ft.Container(
            content = ft.Row(
               controls = [ 
                    ft.Text(f'Today:  {datetime.date.today().strftime("%B %d, %Y")}', color = defaultFontColor, size=16, font_family = 'lato-light'),
                    ft.Text(title, color = defaultFontColor, size = 26, font_family = 'lato-bold'),
                    ft.ElevatedButton(
                        "Add Load", 
                        color = defaultFontColor, 
                        icon=ft.Icons.ADD_ROUNDED, 
                        on_click=add_load_function, 
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            text_style=ft.TextStyle(
                                size=18,
                                font_family = 'lato-regular',
                            ),
                        )
                    ),
                ],
               alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            ),     
        )


"""ADDING NEW LOAD"""   

class NewLoad:
    def __init__(self, page: ft.Page, refresh_callback=None):
        self.page = page
        self.form_fields = {}     
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.selected_date = datetime.date.today()
        self.refresh_callback = refresh_callback
        user_data = SessionManager.get_user_data(page)
        self.user_id = user_data.get('user_id')
        self.access_token = user_data.get('access_token')
        self.supabase = get_supabase_client()
        self._create_form_fields()
        self._create_bottom_sheet_control()
        self._event_handler()


    def _create_form_fields(self):
        # Create form fields
        self.company_input = ft.TextField(label="Company Name")
        self.driver_input = ft.TextField(label="Driver Name")
        self.origin_zip = ft.TextField(label="Origin Zip Code", keyboard_type = ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
        self.origin_city = ft.TextField(label="Origin City")
        self.origin_state = ft.TextField(label="Origin State")
        self.dest_zip = ft.TextField(label="Destination Zip Code", keyboard_type = ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
        self.dest_city = ft.TextField(label="Destination City")
        self.dest_state = ft.TextField(label="Destination State")
        self.miles_driven = ft.TextField(label="Miles Driven", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
        self.deadhead = ft.TextField(label="Deadhead Miles", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",), value="0")
        self.total_miles = ft.TextField(label="Total Miles", read_only=True)
        self.total_rate = ft.TextField(label="Total Rate ($)", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
        self.rate_per_mile = ft.TextField(label="Rate per Mile ($)", read_only=True)
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2020, month=1, day=1),
            on_change=self._date_change_handler)
        
        self.page.overlay.append(self.date_picker)
        
        
    def _create_bottom_sheet_control(self):
        # Define Bottom Sheet
        self.bottom_sheet = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Add New Load", size=20, font_family='lato-bold', color=defaultFontColor),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Pick date",
                            on_click=lambda _: self.page.open(self.date_picker),
                            color=defaultFontColor,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(
                                                    size=16,
                                                    font_family='lato-regular',
                                                )),
                            icon=ft.Icons.CALENDAR_MONTH,
                        ),
                        self.company_input,
                        self.driver_input,
                        ft.Divider(),
                        ft.Text("Origin:"),
                        self.origin_zip,
                        self.origin_city,
                        self.origin_state,
                        ft.Divider(),
                        ft.Text("Destination:"),
                        self.dest_zip,
                        self.dest_city,
                        self.dest_state,
                        ft.Divider(),
                        ft.Text("Load Details:"),
                        self.miles_driven,
                        self.deadhead,
                        self.total_miles,
                        self.total_rate,
                        self.rate_per_mile,
                        ft.Divider(),
                        ft.Row(
                            [
                                ft.ElevatedButton("Cancel", 
                                    on_click=self._close_bottom_sheet, 
                                    style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            text_style=ft.TextStyle(
                                                size=16,
                                                font_family='lato-regular',
                                            )
                                        )),
                                ft.ElevatedButton("Save", on_click=self._save_load, 
                                    style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            text_style=ft.TextStyle(
                                                size=16,
                                                font_family='lato-regular',
                                            )
                                        )),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=600,
                ),
                padding=20,
            ),
        )
        # Add the bottom sheet to the page
        self.page.overlay.append(self.bottom_sheet)
        
    def get_handler(self):
        return self.open_bottom_sheet
    
    # Define Form Displayment Function
    def open_bottom_sheet(self, e):
        self.bottom_sheet.open = True
        self.page.update()
        
    def _close_bottom_sheet(self, e):
        self.bottom_sheet.open = False
        self.page.update()
    
    def _date_change_handler(self, e):
        if self.date_picker.value:
            self.selected_date = self.date_picker.value.strftime("%B %d, %Y")
        self.page.update()
    
    # Define Calculations Function
    def _update_calculations(self, e):
        try:
            miles = float(self.miles_driven.value or 0)
            dh = float(self.deadhead.value or 0)
            total = miles + dh
            self.total_miles.value = str(total)
            
            if total > 0 and self.total_rate.value:
                rate = float(self.total_rate.value or 0)
                self.rate_per_mile.value = f"{rate / total:.2f}"
                
            self.page.update()
        except Exception as ex:
            show_message(self.page, self.error_snackbar, f"Calculation error: {ex}")

    def _fetch_zip_info(self, zip_field, city_field, state_field):
        try:
            zip_code = zip_field.value
            if zip_code and len(zip_code) == 5:
                response = requests.get(f'https://api.zippopotam.us/us/{zip_code}')
                if response.status_code == 200:
                    data = response.json()
                    city_field.value = data['places'][0]['place name']
                    state_field.value = data['places'][0]['state abbreviation']
                    self.page.update()
        except Exception as e:
            print(f"Error fetching zip info: {e}")
            show_message(self.page, self.error_snackbar, f"Error, could not find specified zip {zip_code}")

        
    def _event_handler(self):
        self.miles_driven.on_change = self._update_calculations
        self.deadhead.on_change = self._update_calculations
        self.total_rate.on_change = self._update_calculations
        self.origin_zip.on_change = lambda _: self._fetch_zip_info(self.origin_zip, self.origin_city, self.origin_state)
        self.dest_zip.on_change = lambda _: self._fetch_zip_info(self.dest_zip, self.dest_city, self.dest_state)

    # Define Reset Form Function
    def _reset_form(self):
        self.company_input.value = ""
        self.driver_input.value = ""
        self.origin_zip.value = ""
        self.origin_city.value = ""
        self.origin_state.value = ""
        self.dest_zip.value = ""
        self.dest_city.value = ""
        self.dest_state.value = ""
        self.miles_driven.value = ""
        self.deadhead.value = ""
        self.total_miles.value = ""
        self.total_rate.value = ""
        self.rate_per_mile.value = ""

    async def _save_load(self, e):
        try:
            required_fields = [
                self.company_input, self.driver_input, self.origin_zip, self.origin_city, self.origin_state,
                self.dest_zip, self.dest_city, self.dest_state, self.miles_driven, self.deadhead, self.total_rate
            ]
            # Validator for empty fields
            empty_fields = [field.label for field in required_fields if not field.value]
            if empty_fields:
                show_message(self.page, self.error_snackbar, 'Please fill out all of the fields')
                return 
            self.supabase.postgrest.auth(self.access_token)
            # Adding new load
            new_load = {
                    'date': self.selected_date,
                    "company_name": self.company_input.value or "",
                    "driver_name": self.driver_input.value or "",
                    "origin": f"{self.origin_city.value or ''}, {self.origin_state.value or ''}",
                    "destination": f"{self.dest_city.value or ''}, {self.dest_state.value or ''}",
                    "miles_driven": float(self.miles_driven.value or 0),
                    "deadhead": float(self.deadhead.value or 0),
                    "total_miles": float(self.total_miles.value or 0),
                    "total_rate": float(self.total_rate.value or 0),
                    "rate_per_mile": float(self.rate_per_mile.value or 0),
                    "dispatcher_name": self.user_id,
            }
            supabase = get_supabase_client()
            await supabase.table('Loads').insert(new_load).execute()
            
            
            # Refresh the table if a callback is provided
            if self.refresh_callback is not None:
                print('Refreshing table after adding new load')
                await self.refresh_callback()
                
                
            # Clear form and hide sheet
            self._reset_form()
            self.bottom_sheet.open = False
            self.page.update()
            show_message(self.page, self.success_snackbar, 'New load added successfully.')
            
            
                
               
        except Exception as e:
            print(f'Error saving load: {e}')
            show_message(self.page, self.error_snackbar, f"Make sure all fields are filled and are correct.")

