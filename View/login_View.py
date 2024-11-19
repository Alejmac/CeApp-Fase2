import flet as ft
from flet import *
import os 

from ViewModel.login_ViewModel import LoginViewModel
 

image_path = os.path.join(os.getcwd(), "assets", "entrada1.png")

def on_login_click(page  , registro_field , password_field ):
    login_view_model = LoginViewModel(main_instance=page)
    registro = registro_field.value
    password = password_field.value
    
    if login_view_model.login(registro, password):
        alert = AlertDialog(
            title=Text("Login Exitoso"),
            content=Text("Bienvenido al sistema del CETI"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_alert(page, alert, success=True))
            ]
        )
        page.overlay.append(alert)
        alert.open = True
        page.update()

    else:
        alert = AlertDialog(
            title=Text("Login Fallido"),
            content=Text("Usuario o contraseña incorrectos"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_alert(page, alert, success=False))
            ]
        )
        page.overlay.append(alert)
        alert.open = True
        page.update()

def close_alert(page, alert, success):
    alert.open = False
    page.update()
    if success:
        page.go("/schedule")

def LoginView(page: Page):

    page.window.width = 390
    page.window.height = 844

    page.vertical_alignment = 'start'
    page.horizontal_alignment = "center"

    registro_field = TextField(
        width=280,
        height=100,
        hint_text="Registro",
        border=7,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        color="black",
        prefix_icon=ft.icons.EMAIL
    )

    password_field = TextField(
        width=280,
        height=100,
        hint_text="Contraseña",
        border=7,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        color="black",
        prefix_icon=ft.icons.LOCK,
        password=True
    )

    image_container = Container(
        content=Image(
            src=image_path,
            fit=ft.ImageFit.COVER,
            width=page.width,
            height=100
        ),
        border_radius=ft.border_radius.only(bottom_left=60),
        width=page.width,
        height=250
    )

    login_container = Container(
        Column([
            Container(
                Text(
                    "Iniciar Sesión",
                    width=320,
                    size=30,
                    text_align='center',
                    color="white",
                    weight="w900"
                ),
                padding=ft.padding.only(20, 20)
            ),
            Container(
                registro_field,
                padding=ft.padding.only(20, 20)
            ),
            Container(
                password_field,
                padding=ft.padding.only(20, 20)
            ),
            Container(
                Checkbox(
                    label="Recordar Contraseña",
                    check_color="black",
                    fill_color="white",
                    label_style=ft.TextStyle(color="black") 
                ),
                padding=ft.padding.only(80)
            ),
            Container(
                ElevatedButton(
                    text="INICIAR",
                    width=280,
                    bgcolor="#08406F",
                    on_click=lambda e: on_login_click(page, registro_field, password_field)
                ),
                padding=ft.padding.only(20, 20)
            )
        ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        border_radius=30,
        width=320,
        height=500,
        bgcolor='#E68F59',
        #bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=18,
            blur_radius=15,
            color=ft.colors.BLACK12,
            offset=ft.Offset(0, 5)
        ),
        margin=ft.margin.only(top=-120)  
    )

    # bgcolor=ft.colors.ORANGE_50
    return ft.View("/login", [image_container, login_container],bgcolor=ft.colors.WHITE,vertical_alignment = 'start',horizontal_alignment = "center")

