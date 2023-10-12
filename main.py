# Modulos
import flet as ft
import time

# Base View
class BaseView(ft.View):
    def __init__(
            self,
            page:ft.Page,
            route: str,
            icon: str,
            intro: str,
            footer:str,
            route_to: str,
    ):
        self.page = page
        self.icon = icon
        self.intro = intro
        self.footer = footer
        self.route_to = route_to

        self.image = ft.Icon(
            scale=ft.Scale(4),
            name= self.icon,
            animate_scale=ft.Animation(900, 'decelerate'),
        )

        self.passcode = ft.TextField(
            border_color='white',
            cursor_color='white',
            password=True,
            width=345,
            on_focus= lambda e: self.start_animation(),
            on_blur=lambda e: self.stop_animation(),
        )

        self.running: bool

        super().__init__()

        self.controls=[
            ft.SafeArea(minimum=5,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    alignment='end',
                                    controls=[
                                        ft.IconButton(
                                            scale=0.85,
                                            icon=ft.icons.DARK_MODE_ROUNDED,
                                            on_click=lambda e: self.toggle_theme(e),
                                        ),
                                    ],
                                ),
                                ft.Divider(height=50, color='transparent'),
                                ft.Row(alignment='center', height=200, controls=[self.image]),
                                ft.Row(
                                    alignment='center',
                                    controls=[ft.Text(self.intro,size=16, weight='bold')],
                                ),

                                ft.Divider(height=40, color='transparent'),
                                ft.Row(
                                    alignment='center',
                                    controls=[
                                        ft.Column(
                                            spacing=10,
                                            controls=[
                                                ft.Text('Senha:'),
                                                self.passcode,
                                            ]
                                        )
                                    ]
                                ),

                                ft.Divider(height=180, color='transparent'),
                                ft.Row(alignment='center',
                                       controls=[
                                           ft.Text(
                                               self.footer,
                                               spans=[
                                                   ft.TextSpan(' Aqui!',
                                                               style=ft.TextStyle(italic=True),
                                                               on_click=lambda e: self.routing(),
                                                               )
                                               ]
                                           )
                                       ])
                            ],
                        ),
                        )
        ]

    def routing(self):
        self.stop_animation()
        time.sleep(1.9)
        if self.running == False:
            self.page.go(self.route_to)

    def start_animation(self):
        self.running = True
        self.run_animation()

    def stop_animation(self):
        self.running = False
        self.run_animation()

    def run_animation(self):
        if self.running:
            self.image.scale = ft.transform.Scale(4.9)
            self.image.update()
            time.sleep(0.9)
            self.image.scale = ft.transform.Scale(4)
            self.image.update()
            time.sleep(0.9)
            self.run_animation()

        else:
            self.image.scale = ft.transform.Scale(4)
            self.image.update()


    def toggle_theme(self, e):
        if e.control.icon == ft.icons.LIGHT_MODE_ROUNDED:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.icons.DARK_MODE_ROUNDED
            self.passcode.border_color = 'black'
            self.passcode.cursor_color = 'white'
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.icons.LIGHT_MODE_ROUNDED
            self.passcode.border_color = 'black'
            self.passcode.cursor_color = 'black'
        self.page.update()

class LoginView(BaseView):
    def __init__(self,
                 page: ft.Page,
                 route='/',
                 icon='lock',
                 intro='Bem vindo de volta!',
                 footer='Novo no app? Registre-se!',
                 route_to='/register'
                 ):
        super().__init__(
            page=page,
            route=route,
            icon=icon,
            intro=intro,
            footer=footer,
            route_to=route_to,
        )

# View de Registro
class RegisterView(BaseView):
    def __init__(self,
                 page: ft.Page,
                 route='/register',
                 icon='person_2_sharp',
                 intro='Entre com sua senha',
                 footer='Tudo pronto? Login',
                 route_to='/'
                 ):
        super().__init__(
            page=page,
            route=route,
            icon=icon,
            intro=intro,
            footer=footer,
            route_to=route_to,
        )

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    theme = ft.Theme()
    theme.page_transitions.ios= ft.PageTransitionsTheme.ios
    theme.page_transitions.macos = ft.PageTransitionsTheme.macos
    page.theme = theme

    login = LoginView(page)

    register = RegisterView(page)

    def change_route(route):
        page.views.clear()

        if page.route == '/':
            page.views.append(login)

        if page.route == '/register':
            page.views.append(register)

        page.update()

    page.views.append(login)
    page.on_route_change = change_route

    page.update()

ft.app(main, view=ft.AppView.FLET_APP_WEB)