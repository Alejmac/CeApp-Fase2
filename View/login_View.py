import flet as ft
from flet import *
import os
import asyncio

from ViewModel.login_ViewModel import LoginViewModel
image_path = os.path.join(os.getcwd(), "assets", "entrada1.png")

async def on_login_click(e, page, registro_field, password_field):
    login_view_model = LoginViewModel(main_instance=page)
    registro = registro_field.value
    password = password_field.value

    pb = ft.ProgressBar(width=400)
    progress_text = ft.Text("Iniciando sesión...")
    progress_alert = AlertDialog(
        title=Text("Por favor espere"),
        content=Container(
            content=Column([progress_text, pb]),
            width=300,
            height=150
        ),
        actions=[],
        modal=True  
    )

    page.overlay.append(progress_alert)
    progress_alert.open = True
    page.update()

    async def update_progress_bar():
        for i in range(0, 101):
            pb.value = i * 0.01
            await asyncio.sleep(0.01) 
            page.update()

    async def perform_login():
        if login_view_model.login(registro, password):
            return True
        else:
            return False

    # Ejecutar la barra de progreso y la operacion de login en paralelo
    progress_task = asyncio.create_task(update_progress_bar())
    login_task = asyncio.create_task(perform_login())

    # Esperar a que ambas tareas se completen
    login_success = await login_task
    await progress_task

    if login_success:
        alert = AlertDialog(
            title=Text("Login Exitoso"),
            content=Text("Bienvenido al sistema del CETI"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_alert(page, alert, success=True))
            ],
            modal=True  
        )
    else:
        alert = AlertDialog(
            title=Text("Login Fallido"),
            content=Text("Usuario o contraseña incorrectos"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_alert(page, alert, success=False))
            ],
            modal=True  
        )

    progress_alert.open = False
    page.update()
    page.overlay.append(alert)
    alert.open = True
    page.update()

def print_checkbox_state(e):
    login_view_model = LoginViewModel(main_instance=None)
    login_view_model.save_checkbox_state(e.control.value)
    print(e.control.value)

def close_alert(page, alert, success):
    alert.open = False
    page.update()
    if success:
        page.go("/average")

def LoginView(page: Page):

    page.window.width = 390
    page.window.height = 844

    registro_field = TextField(
        width=280,
        height=100,
        hint_text="Registro",
        border=7,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        color="black",
        prefix_icon=ft.icons.EMAIL
    )

    password_field = TextField(
        width=280,
        height=100,
        hint_text="Contraseña",
        border=7,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
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
        width=page.window.width,
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
                    weight="900"
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
                    label_style=ft.TextStyle(color="black"),
                    on_change=print_checkbox_state
                ),
                padding=ft.padding.only(80)
            ),
            Container(
                ElevatedButton(
                    text="INICIAR",
                    width=280,
                    color="white",
                    bgcolor="#08406F",
                    on_click=lambda e: asyncio.run(on_login_click(e, page, registro_field, password_field))
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
        shadow=ft.BoxShadow(
            spread_radius=18,
            blur_radius=15,
            color=ft.colors.BLACK12,
            offset=ft.Offset(0, 5)
        ),
        margin=ft.margin.only(top=-120)
    )

    return ft.View("/login", [image_container, login_container], bgcolor=ft.colors.WHITE, vertical_alignment='start', horizontal_alignment="center")