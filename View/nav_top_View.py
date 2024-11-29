import flet as ft
from flet import Container, PopupMenuButton, PopupMenuItem, Text, Row, icons, colors
import json
import os


def create_nav_top(page):
    title_text = Text(
  spans=[
                ft.TextSpan(
                    "CeApp",
                    ft.TextStyle(
                        size=25,
                        weight=ft.FontWeight.NORMAL,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 20), (150, 20), [ft.colors.ORANGE_900, ft.colors.ORANGE_100]
                            )
                        ),
                    ),
                ),
            ],
    )

    # Crear el NavigationDrawer
    navigation_drawer = ft.NavigationDrawer(
        on_dismiss=lambda e: page.add(ft.Text("Drawer dismissed")),
        on_change=lambda e: handle_navigation_change(e, page),
        controls=[
            ft.NavigationDrawerDestination(icon=ft.icons.PERSON, label="Data Alumno"),
            ft.NavigationDrawerDestination(icon=ft.icons.EXIT_TO_APP, label="Salir"),
        ],
    )

    page.navigation_drawer = navigation_drawer

    # Función  en el NavigationDrawer
    def handle_navigation_change(e, page):
        if e.control.selected_index == 0:
            page.go("/data_alumno")
        elif e.control.selected_index == 1:
            page.go("/salir")

    # Crear el PopupMenuButton
    popup_menu_button = PopupMenuButton(
        items=[
            PopupMenuItem(icon=ft.icons.PERSON,text="Datos del Alumno", on_click=lambda _: page.go("/data_student")),
            PopupMenuItem(icon=ft.icons.EXIT_TO_APP,text="Salir", on_click=lambda _: (ModificarJson(), page.go("/login")) ),
        ]
    )

    # Crear el contenedor
    nav_top_container = Container(
        content=Row(
            controls=[
                title_text,
                popup_menu_button
            ],
            alignment="spaceBetween"
        ),
        bgcolor="#f5f5f5",
        height=60,
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        border=ft.Border(bottom=ft.BorderSide(0.3, ft.colors.GREY)),  # Agregar borde inferior
        margin=ft.margin.only(top=20) 
        
    )
    def ModificarJson():
        data_folder = os.path.join(os.getcwd(), "Data")

        file_path = os.path.join(data_folder, "active.json")
        with open(file_path, 'w') as file:
                json.dump({"active": False}, file)
                print("se modifico el estado del json")  

 
    # Devolver el contenedor
    return nav_top_container

# Exportar la función para que pueda ser importada en otros archivos
__all__ = ["create_nav_top"]