# Imports
import flet as ft 
from flet_route import Params, Basket
from config import supabase
from assets.styles import *
import pandas as pd
import datetime
import math
from helper_functions import show_message, create_snackbar, create_logo, create_sidebar, add_load, create_header


class DispatcherMain:
    def __init__(self):
        self.error_snackbar = create_snackbar(ft.Colors.RED_600)
        self.success_snackbar = create_snackbar(ft.Colors.GREEN_600)
        self.supabase = supabase
    
    
    # Create Chart Function
    def create_weekly_chart(self, agg_function, left_axis_label_func, stroke_color, title):
        res = self.supabase.table('Loads').select(
            'date, total_rate'
        ).gte(
            'date', str(self.this_monday)
        ).lt(
            'date', str(self.next_monday)
        ).eq(
            'dispatcher_name', self.user_id
        ).execute()

        empty_data = {'date': [], 'total_rate': []}
        df = pd.DataFrame(empty_data)

        df = pd.concat([df, pd.DataFrame(res.data)], ignore_index=True)

        # Data Manipulation
        df['date'] = pd.to_datetime(df['date'])
        df['weekday'] = df['date'].dt.weekday
        daily_totals = df.groupby('weekday')['total_rate'].agg(agg_function).to_dict()
        
        # Set max y-axis value
        max_rate = max(daily_totals.values(), default=0)
        if agg_function == 'sum':
            y_max_chart = math.ceil(max_rate / 1000) * 1000 if max_rate > 0 else 1000 
        elif agg_function == 'count':
            y_max_chart = max_rate + 1
        y_interval = y_max_chart / 5

        # Data Points
        data_points = [
            ft.LineChartDataPoint(x=i, y=daily_totals.get(i, 0))
            for i in range(7)
        ]

        # Define Line Data
        line_data = ft.LineChartData(
            data_points=data_points,
            stroke_width=4,
            color=stroke_color,
            stroke_cap_round=True,
            curved=True,
            below_line_gradient = ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.with_opacity(0.3, stroke_color),
                    'transparent'
                ]
            )
        )

        # Axes
        bottom_axis_labels = [
            ft.ChartAxisLabel(value=0, label=ft.Text("Mon")),
            ft.ChartAxisLabel(value=1, label=ft.Text("Tue")),
            ft.ChartAxisLabel(value=2, label=ft.Text("Wed")),
            ft.ChartAxisLabel(value=3, label=ft.Text("Thu")),
            ft.ChartAxisLabel(value=4, label=ft.Text("Fri")),
            ft.ChartAxisLabel(value=5, label=ft.Text("Sat")),
            ft.ChartAxisLabel(value=6, label=ft.Text("Sun")),
        ]
        left_axis_labels = [
            ft.ChartAxisLabel(
                value=i * y_interval,
                label=ft.Text(left_axis_label_func(i*y_interval), size=12)
            )
            for i in range(6)
        ]

        # Create Chart
        chart = ft.LineChart(
            data_series=[line_data],
            border=ft.Border(bottom=ft.BorderSide(2, ft.Colors.with_opacity(0.8, defaultFontColor))),
            left_axis=ft.ChartAxis(labels=left_axis_labels, labels_size=40),
            bottom_axis=ft.ChartAxis(labels=bottom_axis_labels, show_labels=True, labels_size=40, labels_interval=1),
            tooltip_bgcolor=ft.Colors.with_opacity(0.0, defaultBackgroundColor),
            min_y=0,
            max_y=y_max_chart,
            min_x=0,
            max_x=6,
        )

        return ft.Container(
            expand = 5,
            height = 300,
            padding = 30,
            content=ft.Column([
                ft.Text(title, font_family='lato-bold', size=20),
                chart
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,              
            spacing=10),
        )
        
    
    # Define Page View
    def view(self, page: ft.Page, params: Params, basket: Basket):
        
        # Set page parameters
        page.window.maximized = True
        page.window.min_height = minWindowHeight
        page.window.min_width = minWindowWidth
        page.title = 'TruckOps - Dashboard'
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
        
        
        today = datetime.date.today()
        date_since_monday = today.weekday()
        self.this_monday = today - datetime.timedelta(days=date_since_monday)
        self.next_monday = self.this_monday + datetime.timedelta(days=7)
        
        
        # Define Load Count
        def count_loads(self, this_monday, next_monday):
            n_loads = self.supabase.table('Loads').select('*', count='exact').gte('date', str(this_monday)).lt('date', str(next_monday)).eq('dispatcher_name', self.user_id).execute()    
            return n_loads.count
        
    
        # Define Rate Sum
        def sum_weekly_rate(self, this_monday, next_monday):
            res = self.supabase.table('Loads').select('total_rate').gte('date', str(this_monday)).lt('date', str(next_monday)).eq('dispatcher_name', self.user_id).execute()    
            return sum(row['total_rate'] for row in res.data if row['total_rate'] is not None)
        
        
        # Define Rate Sum
        def top_rate(self, this_monday, next_monday):
            rates = self.supabase.table('Loads').select('total_rate').gte('date', str(this_monday)).lt('date', str(next_monday)).eq('dispatcher_name', self.user_id).execute()    
            return max([row['total_rate'] for row in rates.data if row['total_rate'] is not None], default=0)
            
        
        # Weekly Statistics Container
        weekly_stats = ft.Container(
            expand = 2,
            padding = 30,
            content = ft.Row(
                spacing = 60,
                controls = [
                    ft.Container(
                        expand = 2,
                        alignment = ft.alignment.center,
                        bgcolor = defaultButtonColor,
                        border_radius = 10,
                        content = ft.Column(
                            controls = [    
                                ft.Text('Total Loads This Week', color = defaultFontColor, size=bodyFontSize, font_family='lato-light'),
                                ft.Text(count_loads(self, self.this_monday, self.next_monday), color = defaultFontColor, size=statsFontsize, font_family='lato-bold'),
                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    ),
                    ft.Container(
                        expand = 2,
                        alignment = ft.alignment.center,
                        bgcolor = defaultButtonColor,
                        border_radius = 10,
                        content = ft.Column(
                            controls = [    
                                ft.Text('Total Rate This Week', color = defaultFontColor, size=bodyFontSize, font_family='lato-light'),
                                ft.Text(f'$ {sum_weekly_rate(self, self.this_monday, self.next_monday)}', color = defaultFontColor, size=statsFontsize, font_family='lato-bold'),
                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    ),
                    ft.Container(
                        expand = 2,
                        alignment = ft.alignment.center,
                        bgcolor = defaultButtonColor,
                        border_radius = 10,
                        content = ft.Column(
                            controls = [    
                                ft.Text('Top Rate of This Week', color = defaultFontColor, size=bodyFontSize, font_family='lato-light'),
                                ft.Text(f'$ {top_rate(self, self.this_monday, self.next_monday)}', color = defaultFontColor, size=statsFontsize, font_family='lato-bold'),
                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    ),
                    ft.Container(
                        expand = 2,
                        alignment = ft.alignment.center,
                        bgcolor = defaultButtonColor,
                        border_radius = 10,
                        content = ft.Column(
                            controls = [    
                                ft.Text('Currently Active Loads', color = defaultFontColor, size=bodyFontSize, font_family='lato-light'),
                                ft.Text('Coming Soon', color = defaultFontColor, size=statsFontsize, font_family='lato-bold'),
                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    ),  
                ],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )
        

        return ft.View(
            '/dashboard',
            bgcolor = defaultBackgroundColor,
            padding = ft.padding.all(15),
            controls = [
                ft.Row(
                    expand = True,
                    controls = [
                        # Sidebar
                        ft.Container(
                            expand = 1,
                            content=ft.Column(
                                controls=[
                                    # Logo Container
                                    ft.Container(
                                        content=create_logo(140, 80),
                                        alignment=ft.alignment.center,
                                        width=200
                                    ),
                                    create_sidebar(page, font_family='lato-light')
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ),
                        # Divider
                        ft.VerticalDivider(width=1),
                        # Main content
                        ft.Container(
                            expand = 9,
                            content = ft.Column(
                                controls = [
                                    create_header('Dashboard', add_load(self, page)),
                                    ft.Divider(),
                                    weekly_stats,
                                    ft.Row(
                                        expand=8,
                                        controls = [
                                            self.create_weekly_chart('sum', lambda y: f"${int(y/1000)}k", ft.Colors.TEAL, 'Daily Total Rate (Current Week)'),
                                            self.create_weekly_chart('count', lambda y: f"{int(y)}", ft.Colors.BLUE, 'Daily Load Volume (Current Week)')
                                        ]
                                    )
                                ],
                                expand=True
                            )
                        )
                    ]
                )        
            ]
        )
    
    