# Imports
import flet as ft
from flet_route import Params, Basket
from assets.styles import *
from helper_functions import show_message, create_snackbar, create_logo


class SetupDBPage:
    def __init__(self):
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)
    
    # Define Greeting Text
    welcome_text = ft.Container(
        content=ft.Text(
            'Enter your database URL and KEY',
            size=titleFontSize,
            color=defaultFontColor,
            font_family='lato-bold',
        ),
        alignment=ft.alignment.center
    )
    
    # Define Email Input Field 
    url_input = ft.Container(
        width=400,
        content = ft.TextField(
            label = 'URL',
            hint_text = 'Enter your Supabase project URL',
            expand=False,
            bgcolor = defaultBackgroundColor2,
            border = ft.InputBorder.NONE
        ), 
        border_radius = 15,
    )
    
    # Define Password Input Field
    key_input = ft.Container(
        width=400,
        content = ft.TextField(
            label = 'KEY',
            hint_text = 'Enter your Supabase key',
            bgcolor = defaultBackgroundColor2,
            border = ft.InputBorder.NONE
        ),
        border_radius = 15,
    )
    
    def connect(self, e, page):
        # Retrieve Values from Inputs 
        url = self.url_input.content.value
        key = self.key_input.content.value

        # Validators 
        if not url or not key:
            show_message(page, self.error_snackbar, 'Please fill in all fields.')
            return
        # Register User if Success
        try:
            env_file_path = '.env'
            with open(env_file_path, 'w') as f:
                f.write(f'SUPABASE_URL={url}\n')
                f.write(f'SUPABASE_KEY={key}\n')
                f.close()
                show_message(page, self.success_snackbar, 'You successfully connected to database!')
        except Exception as error:
            show_message(page, self.error_snackbar, f"Connecting failed: {str(error)}")

    
    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        
        # Define Page Parameters
        page.title = 'TruckOps - Setup Database'
        page.window.min_height = loginWindowHeight
        page.window.min_width = loginWindowWidth
        page.fonts = {'lato-bold': 'assets/Lato-Bold.ttf',
                      'lato-light': 'assets/Lato-Light.ttf'}
        page.snack_bar = self.error_snackbar
        
        # Define Connect Button
        connect_button = ft.Container(
            ft.Text(
                'Connect', 
                color = defaultFontColor,
                size = buttonFontSize,
                font_family='lato-light',
            ),
            on_click = lambda e: self.connect(e, page),
            width = 300,
            height = 40,
            alignment = ft.alignment.center,
            bgcolor = defaultButtonColor,   
            border_radius = 15,
        )
        
        return ft.View(
            '/setup_db',
            padding = ft.padding.all(15),
            controls = [
                ft.Row(
                    expand = True,
                    controls = [
                        # Container with All Content
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                alignment = ft.MainAxisAlignment.CENTER,
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                controls = [
                                    create_logo(140, 80),
                                    self.welcome_text,
                                    self.url_input,
                                    self.key_input,
                                    connect_button,
                                    ft.Row(
                                        controls = [
                                            ft.Container(
                                                ft.Text(
                                                    'Back to Login', 
                                                    color=defaultFontColor,
                                                    font_family='lato-light',
                                                ),
                                                on_click=lambda x: page.go('/'),
                                                alignment=ft.alignment.center,
                                                height=25,          
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=5
                                    )
                                ],
                                spacing = 15
                            )
                        )
                    ]
                )   
            ]
        )