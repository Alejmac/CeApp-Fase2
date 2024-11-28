import flet as ft
from flet import CupertinoNavigationBar, NavigationBarDestination, icons,ElevatedButton, Border, BorderSide

def create_nav_bar(page):
    nav_bar = CupertinoNavigationBar(
        bgcolor="#08406F",
        inactive_color=ft.colors.GREY,
       #active_color=ft.colors.RED,
        on_change=lambda e: handle_navigation(page, e.control.selected_index),
        destinations=[
            NavigationBarDestination(icon=icons.GRADE, label="Promedio"),
            NavigationBarDestination(icon=icons.SCHEDULE, label="Horario"),
            NavigationBarDestination(icon=icons.CALENDAR_VIEW_DAY, label="Calificaciones"),
            NavigationBarDestination(icon=icons.PEOPLE, label="Materias")
        ],
        border=ft.border.all(0.3, ft.colors.GREY)  
    )
    return nav_bar

def handle_navigation(page, index):
    routes = ["/average","/schedule", "/qualifications", "/teachers"]
    if index < len(routes):
        page.go(routes[index])

# Exportar la función para que pueda ser importada en otros archivos
__all__ = ["create_nav_bar"]
