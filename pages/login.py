# Imports
import asyncio
import os
import flet as ft
#from config import supabase
from config import supabase
from flet_route import Params, Basket
from assets.styles import *
from helper_functions import show_message, validate_email, create_snackbar, create_logo


class LoginPage:
    def __init__(self, supabase):
        self.supabase = supabase
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)

    # Define Greeting Text
    welcome_text = ft.Container(
            content=ft.Text(
                'Welcome Back!',
                size=titleFontSize,
                color=defaultFontColor,
                font_family='lato-bold',
            ),
            alignment=ft.alignment.center
        )
    
    # Define Email Input Field 
    login_input = ft.Container(
        width=400,
        content = ft.TextField(
            label = 'Email',
            hint_text = 'Enter your email address',
            expand=False,
            bgcolor = defaultBackgroundColor2,
            border = ft.InputBorder.NONE,
        ),
        border_radius = 15,
    )
    
    # Define Password Input Field 
    password_input = ft.Container(
        width=400,
        content = ft.TextField(
            label = 'Password',
            hint_text = 'Enter password',
            password = True,
            can_reveal_password = True,
            bgcolor = defaultBackgroundColor2,
            border = ft.InputBorder.NONE,
        ),
        border_radius = 15,
    )


    # Define Login Function
    async def login(self, e, page: ft.Page):
        # Access the page object from the event
        print(f'Retrieving session data if available...')

        email = self.login_input.content.value
        password = self.password_input.content.value

        if not email or not password:
            show_message(page, self.error_snackbar, 'Please enter email and password.')
            return

        if not validate_email(email):
            show_message(page, self.error_snackbar, "Please enter a valid email address.")
            return

        def reset_form():
            self.password_input.content.value = ''

        try:
            print('Attempting to log in...')
            response = await self.supabase.auth.sign_in_with_password({'email': email, 'password': password})
            session = response.session
            user_id = response.user.id
            print(f"✅ Supabase auth successful for user: {user_id}")
            page.session.set('user_id', user_id)
            page.session.set('access_token', session.access_token)
            page.session.set('refresh_token', session.refresh_token)
            print(f"User ID: {page.session.get('user_id')}")
            print(f"✅ Session data stored successfully")
            # TEMP SOLLUTION
            with open('storage/session.txt', 'w') as f:
                f.write(f'ACCESS_TOKEN={session.access_token}\n')
                f.write(f'REFRESH_TOKEN={session.refresh_token}\n')
                f.write(f'U_ID={user_id}\n')
                f.close()
            print(f'Session data stored in file.')
            reset_form()
            page.go('/dashboard')
        except Exception as error:
            show_message(page, self.error_snackbar, "Login failed: Invalid credentials.")
            print(f"Login error: {error}")

            

    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        
        # Define Page Parameters
        page.title = 'TruckOps - Login'
        page.window.min_height = loginWindowHeight
        page.window.min_width = loginWindowWidth
        page.fonts = {'lato-bold': 'assets/Lato-Bold.ttf', 'lato-regular': 'assets/Lato-Regular.ttf',
                      'lato-light': 'assets/Lato-Light.ttf'}
        page.snack_bar = self.error_snackbar
        
        async def login_wrapper(e):
            # Show loading state
            login_button.content = ft.ProgressRing(width=20, height=20, color=defaultFontColor)
            login_button.update()
            
            try:
                await self.login(e, page)
            finally:
                # Restore button text
                login_button.content = ft.Text(
                    'Login', 
                    color=defaultFontColor,
                    font_family='lato-light',
                    size=buttonFontSize
                )
                login_button.update()
        
        # Define Login Button
        login_button = ft.Container(
            ft.Text(
                'Login', 
                color = defaultFontColor,
                font_family='lato-light',
                size = buttonFontSize
            ),
            on_click = login_wrapper,
            width = 300,
            height = 40,
            alignment = ft.alignment.center,
            bgcolor = defaultButtonColor,
            border_radius = 15,
        )
        
        
        # Define Link Button
        def create_link_button(text, route):
            return ft.Container(
                ft.Text(
                    text,
                    color=defaultFontColor,
                    font_family='lato-light',
                ),
                on_click=lambda _: page.go(route),
                alignment=ft.alignment.center,
                height=25,
            )
        
        
        return ft.View(
            '/',
            padding = ft.padding.all(15),
            controls = [
                ft.Row(
                    expand = True,
                    controls = [
                        # Main Container for Page's Content
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                alignment = ft.MainAxisAlignment.CENTER,
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                controls = [
                                    create_logo(140, 80),
                                    self.welcome_text,
                                    self.login_input,
                                    self.password_input,
                                    login_button,
                                    ft.Row(
                                        controls = [
                                            create_link_button('Create an account', '/signup'),
                                            ft.Text(' | ',color=defaultFontColor,font_family='lato-light',size=smallFontSize),
                                            create_link_button('Forgot Password', '/renew'),
                                        ],
                                        alignment = ft.MainAxisAlignment.CENTER,
                                    )
                                ],
                                spacing = 15
                            )
                        )
                    ]
                )  
            ]
        )