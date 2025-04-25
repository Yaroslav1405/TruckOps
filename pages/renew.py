import flet as ft
from config import supabase
from flet_route import Params, Basket
from assets.styles import *
from helper_functions import show_message, validate_email, create_snackbar, create_logo

class RenewCredentials:
    def __init__(self):
        self.supabase = supabase
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)
        
    # Define Greeting Text
    welcome_text = ft.Container(
            content=ft.Text(
                'Reset Password',
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
            hint_text = 'Enter your email address',
            expand=False,
            bgcolor = defaultBackgroundColor2,
            border = ft.InputBorder.NONE,
        ),
        border_radius = 15,
    )
    
    
    # Define Reset Link
    def send_reset_link(self, e, page):
        email = self.email_input.content.value
        
        # Validators 
        if not email:
            show_message(page, self.error_snackbar, 'Please enter your email address.')
            return
    
        if not validate_email(email):
            show_message(page, self.error_snackbar, 'Please enter a valid email address.')
            return
        
        def reset_form():
            self.email_input.content.value = ''

        # Send Link if Success
        try: 
            self.supabase.auth.api.reset_password_for_email(email)
            show_message(page, self.success_snackbar, 'Password reset link sent! Please check your inbox.')
            reset_form()
        except Exception as error:
            show_message(page, self.error_snackbar, f'Failed to send reset email. Please try again.')
        
        
    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = 'TruckOps - Renew Credentials'
        page.window.min_height = loginWindowHeight
        page.window.min_width = loginWindowWidth
        page.fonts = {'lato-bold': 'assets/Lato-Bold.ttf', 'lato-regular': 'assets/Lato-Regular.ttf',
                      'lato-light': 'assets/Lato-Light.ttf'}
        page.snack_bar = self.error_snackbar
        
        # Submit Button
        submit_button = ft.Container(
            ft.Text(
                'Send Reset Link',
                color = defaultFontColor,
                size = buttonFontSize,
                font_family='lato-light',
            ),
            on_click = lambda e: self.send_reset_link(e, page),
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
                    color = defaultFontColor,
                    size = smallFontSize,
                    font_family='lato-light',
                ),
                on_click = lambda e: page.go(route),
                alignment = ft.alignment.center,
            )
        
        return ft.View(
            '/renew',
            padding = ft.padding.all(15),
            controls = [
                ft.Row(
                    expand = True,
                    controls=[
                        ft.Container(
                            expand=2,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls = [
                                    create_logo(140, 80),
                                    self.welcome_text,
                                    ft.Text(
                                        "Please enter your email to get a password reset link.",
                                        color=defaultFontColor,
                                        font_family='lato-light',
                                        text_align=ft.TextAlign.CENTER,
                                        size=smallFontSize
                                    ),
                                    self.email_input,
                                    submit_button,
                                    ft.Row(
                                        controls = [
                                            create_link_button('Login', '/'),
                                            ft.Text(' | ', color=defaultFontColor, font_family='lato-light', size=smallFontSize),
                                            create_link_button('Create an account', '/signup')
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