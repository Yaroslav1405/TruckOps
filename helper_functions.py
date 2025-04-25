# Imports
import flet as ft
import re
import requests
import datetime
from assets.styles import *


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
    
    #Logout functionality
    def logout(e):
        page.client_storage.remove('user_id')
        page.go('/')
    
    # Text Styles 
    text_style = {'size': 18, 'color': defaultFontColor}
    
    # Font 
    if font_family:
        text_style['font_family'] = font_family
    
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
                        on_click=logout,
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
def create_header(title: str, on_add_load: callable) -> ft.Container:
    return ft.Container(
            content = ft.Row(
               controls = [ 
                    ft.Text(f'Today:  {datetime.date.today().strftime("%B %d, %Y")}', color = defaultFontColor, size=16, font_family = 'lato-light'),
                    ft.Text(title, color = defaultFontColor, size = 26, font_family = 'lato-bold'),
                    ft.ElevatedButton(
                        "Add Load", 
                        color = defaultFontColor, 
                        icon=ft.Icons.ADD_ROUNDED, 
                        on_click=on_add_load, 
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

# Create form fields
company_input = ft.TextField(label="Company Name")
driver_input = ft.TextField(label="Driver Name")
origin_zip = ft.TextField(label="Origin Zip Code", keyboard_type = ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
origin_city = ft.TextField(label="Origin City")
origin_state = ft.TextField(label="Origin State")
dest_zip = ft.TextField(label="Destination Zip Code", keyboard_type = ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
dest_city = ft.TextField(label="Destination City")
dest_state = ft.TextField(label="Destination State")
miles_driven = ft.TextField(label="Miles Driven", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
deadhead = ft.TextField(label="Deadhead Miles", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",), value="0")
total_miles = ft.TextField(label="Total Miles", read_only=True)
total_rate = ft.TextField(label="Total Rate ($)", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"[0-9+]", allow=True, replacement_string="",))
rate_per_mile = ft.TextField(label="Rate per Mile ($)", read_only=True)
        

def add_load(self, page: ft.Page, refresh_callback = None):
    access_token = page.client_storage.get('access_token')

    # Define Calculations Function
    def update_calculations(e):
        try:
            miles = float(miles_driven.value or 0)
            dh = float(deadhead.value or 0)
            total = miles + dh
            total_miles.value = str(total)
            
            if total > 0 and total_rate.value:
                rate = float(total_rate.value or 0)
                rate_per_mile.value = f"{rate / total:.2f}"
                
            page.update()
        except Exception as ex:
            show_message(page, self.error_snackbar, f"Calculation error: {ex}")

    # Connect Calculation Functions
    miles_driven.on_change = update_calculations
    deadhead.on_change = update_calculations
    total_rate.on_change = update_calculations


    # Define ZIP Lookup Function
    def fetch_zip_info(e, zip_field, city_field, state_field):
        try:
            zip_code = zip_field.value
            if zip_code and len(zip_code) == 5:
                response = requests.get(f'https://api.zippopotam.us/us/{zip_code}')
                if response.status_code == 200:
                    data = response.json()
                    city_field.value = data['places'][0]['place name']
                    state_field.value = data['places'][0]['state abbreviation']
                    page.update()
        except Exception as e:
            show_message(page, self.error_snackbar, f"Error, could not find specified zip {zip_code}")

    # Connect ZIP Lookup Events
    origin_zip.on_change = lambda e: fetch_zip_info(e, origin_zip, origin_city, origin_state)
    dest_zip.on_change = lambda e: fetch_zip_info(e, dest_zip, dest_city, dest_state)


    # Define Change of Date Format
    def handle_change(e):
        self.selected_date = e.control.value.strftime("%B %d, %Y")
        page.update()
        
            
    # Define Load Save Function
    def save_load(e):
        try:
            required_fields = [
                company_input, driver_input, origin_zip, origin_city, origin_state,
                dest_zip, dest_city, dest_state, miles_driven, deadhead, total_rate
            ]
            # Validator for empty fields
            empty_fields = [field.label for field in required_fields if not field.value]
            if empty_fields:
                show_message(page, self.error_snackbar, 'Please fill out all of the fields')
                return 
            self.supabase.postgrest.auth(access_token)
            # Adding new load
            new_load = {
                    'date': self.selected_date,
                    "company_name": company_input.value or "",
                    "driver_name": driver_input.value or "",
                    "origin": f"{origin_city.value or ''}, {origin_state.value or ''}",
                    "destination": f"{dest_city.value or ''}, {dest_state.value or ''}",
                    "miles_driven": float(miles_driven.value or 0),
                    "deadhead": float(deadhead.value or 0),
                    "total_miles": float(total_miles.value or 0),
                    "total_rate": float(total_rate.value or 0),
                    "rate_per_mile": float(rate_per_mile.value or 0),
                    "dispatcher_name": self.user_id,
            }
            self.supabase.table('Loads').insert(new_load).execute()
            
            # Clear form and hide sheet
            reset_form()
            bottom_sheet.open = False
            page.update()
            show_message(page, self.success_snackbar, 'New load added successfully.')
            
            # Refresh the table if a callback is provided
            if refresh_callback:
                refresh_callback()
               
        except Exception:
            show_message(page, self.error_snackbar, f"Make sure all fields are filled and are correct.")


    # Define Reset Form Function
    def reset_form():
        company_input.value = ""
        driver_input.value = ""
        origin_zip.value = ""
        origin_city.value = ""
        origin_state.value = ""
        dest_zip.value = ""
        dest_city.value = ""
        dest_state.value = ""
        miles_driven.value = ""
        deadhead.value = ""
        total_miles.value = ""
        total_rate.value = ""
        rate_per_mile.value = ""


    # Define Bottom Sheet
    bottom_sheet = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Add New Load", size=20, font_family='lato-bold', color=defaultFontColor),
                    ft.Divider(),
                    ft.ElevatedButton(
                        "Pick date",
                        on_click=lambda e: page.open(
                            ft.DatePicker(
                                first_date=datetime.datetime(year=2020, month=1, day=1),
                                on_change=handle_change,
                            )
                        ),
                        color=defaultFontColor,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(
                                                size=16,
                                                font_family='lato-regular',
                                            )),
                        icon=ft.Icons.CALENDAR_MONTH,
                    ),
                    company_input,
                    driver_input,
                    ft.Divider(),
                    ft.Text("Origin:"),
                    origin_zip,
                    origin_city,
                    origin_state,
                    ft.Divider(),
                    ft.Text("Destination:"),
                    dest_zip,
                    dest_city,
                    dest_state,
                    ft.Divider(),
                    ft.Text("Load Details:"),
                    miles_driven,
                    deadhead,
                    total_miles,
                    total_rate,
                    rate_per_mile,
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.ElevatedButton("Cancel", 
                                on_click=lambda e: setattr(bottom_sheet, "open", False) or page.update(), 
                                style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        text_style=ft.TextStyle(
                                            size=16,
                                            font_family='lato-regular',
                                        )
                                    )),
                            ft.ElevatedButton("Save", on_click=save_load, 
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
        open=False,
    )


    # Define Form Displayment Function
    def show_form(e):
        if not self.user_id or not access_token:
            show_message(page, self.error_snackbar, "Please log in to add a load.")
            page.go('/')
            return
        bottom_sheet.open = True
        page.update()

    # Add the bottom sheet to the page
    page.overlay.append(bottom_sheet)
    page.update()
    
    return show_form