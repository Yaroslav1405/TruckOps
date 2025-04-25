# Imports
import os
import flet as ft
#from config import supabase
from config import supabase
from flet_route import Params, Basket
from assets.styles import *
from helper_functions import show_message, validate_email, create_snackbar, create_logo


class LoginPage:
    def __init__(self):
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
    def login(self, e, page):
        # Retrieve Values from Inputs 
        email = self.login_input.content.value
        password = self.password_input.content.value

        # Validators
        if not email or not password:
            show_message(page, self.error_snackbar, 'Please enter email and password.')
            return

        if not validate_email(email):
            show_message(page, self.error_snackbar, "Please enter a valid email address.")
            return


        # Define Reset Form
        def reset_form():
            self.password_input.content.value = ''

        # Log in User if Success
        try:
            response = self.supabase.auth.sign_in_with_password({'email': email, 'password': password})
            session = response.session
            user_id = response.user.id
            page.client_storage.set('user_id', user_id)
            page.client_storage.set('access_token', session.access_token)
            page.client_storage.set('refresh_token', session.refresh_token)
            reset_form()
            page.go('/dashboard')  
        except Exception as error:
            show_message(page, self.error_snackbar, "Login failed: Invalid credentials.")


    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        
        # Define Page Parameters
        page.title = 'TruckOps - Login'
        page.window.min_height = loginWindowHeight
        page.window.min_width = loginWindowWidth
        page.fonts = {'lato-bold': 'assets/Lato-Bold.ttf', 'lato-regular': 'assets/Lato-Regular.ttf',
                      'lato-light': 'assets/Lato-Light.ttf'}
        page.snack_bar = self.error_snackbar
        
        # Define Login Button
        login_button = ft.Container(
            ft.Text(
                'Login', 
                color = defaultFontColor,
                font_family='lato-light',
                size = buttonFontSize
            ),
            on_click = lambda e: self.login(e, page),
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