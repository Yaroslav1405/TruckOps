# Imports
import flet as ft
from config import supabase
from flet_route import Params, Basket
from assets.styles import *
from helper_functions import show_message, validate_email, create_snackbar, create_logo


class SignupPage:
    def __init__(self):
        self.supabase = supabase
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)
    
    # Define Greeting Text
    welcome_text = ft.Container(
            content=ft.Text(
                'Create an Account',
                size=titleFontSize,
                color=defaultFontColor,
                font_family='lato-bold',
            ),
            alignment=ft.alignment.center
        )
    
    # Define Email Input Field 
    email_input = ft.Container(
        width=400,
        content = ft.TextField(
            label = 'Email',
            hint_text = 'Enter email address',
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
    
    
    # Define Password Confirmation Input
    confirm_password_input = ft.Container(
        width=400,
        content = ft.TextField(
            label = 'Confirm Password',
            hint_text = 'Confirm password',
            password = True,
            can_reveal_password = True,
            bgcolor = defaultBackgroundColor2,
            border = ft.InputBorder.NONE,
        ),
        border_radius = 15,
    )
    
    
    def signup(self, e, page):
        # Retrieve Values from Inputs 
        email = self.email_input.content.value
        password = self.password_input.content.value
        confirm_password = self.confirm_password_input.content.value

        # Validators 
        if not email or not password or not confirm_password:
            show_message(page, self.error_snackbar, 'Please fill in all fields.')
            return

        if not validate_email(email):
            show_message(page, self.error_snackbar, 'Please enter a valid email address.')
            return

        if password != confirm_password:
            show_message(page, self.error_snackbar, "Passwords don't match.")
            return

        if len(password) < 6:
            show_message(page, self.error_snackbar, "Password must be at least 6 characters long.")
            return
        # Register User if Success
        try:
            response = self.supabase.auth.sign_up({'email': email, 'password': password})
            if response.user:
                show_message(page, self.success_snackbar, 'You successfully registered an account!')
                page.go('/')
        except Exception as error:
            show_message(page, self.error_snackbar, f"Signup failed: {str(error)}")

    
    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        
        # Define Page Parameters
        page.title = 'TruckOps - Signup Page'
        page.window.min_height = loginWindowHeight
        page.window.min_width = loginWindowWidth
        page.fonts = {'lato-bold': 'assets/Lato-Bold.ttf', 'lato-regular': 'assets/Lato-Regular.ttf',
                      'lato-light': 'assets/Lato-Light.ttf'}
        page.snack_bar = self.error_snackbar
        
        # Define Signup Button
        signup_button = ft.Container(
            ft.Text(
                'Sign up', 
                color = defaultFontColor,
                size = buttonFontSize,
                font_family='lato-light',
            ),
            on_click = lambda e: self.signup(e, page),
            width = 300,
            height = 40,
            alignment = ft.alignment.center,
            bgcolor = defaultButtonColor,   
            border_radius = 15,
        )
        
        return ft.View(
            '/signup',
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
                                    self.email_input,
                                    self.password_input,
                                    self.confirm_password_input,
                                    signup_button,
                                    ft.Row(
                                        controls = [
                                            ft.Text(
                                                'Already have an account?',
                                                color=defaultFontColor,
                                                font_family='lato-light',
                                                size=smallFontSize
                                            ),
                                            ft.Container(
                                                ft.Text(
                                                    'Login', 
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
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            'Connect to database',
                                            color=defaultFontColor,
                                            font_family='lato-light',
                                        ),
                                        on_click = lambda x: page.go('/setup_db'),
                                        alignment=ft.alignment.center,
                                        height=25,
                                    )
                                ],
                                spacing = 15
                            )
                        )
                    ]
                )   
            ]
        )