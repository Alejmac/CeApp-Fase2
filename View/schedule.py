import flet as ft
from flet import Page, Column, Text, Container, Tabs, Tab, DataTable, DataColumn, DataRow, DataCell, ListView,View
from View.nav_top_View import create_nav_top
from View.nav_bar_View import create_nav_bar   
from ViewModel.schedule_ViewModel import ScheduleViewModel   
import os

def create_tab_content(day_schedule):

    data_table = create_data_table(day_schedule)
    list_view = ListView(
        controls=[data_table],
        expand=True
    )

    # Crear un contenedor blanco que contenga el ListView
    container = Container(
        content=list_view,
        bgcolor=ft.colors.WHITE,
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(10),
        expand=True,
        margin=ft.margin.only(top=0, bottom=20)  # Margen superior de 20 píxeles
    )

    return container

def create_data_table(day_schedule):
    # Crear las columnas del DataTable
    columns = [
        DataColumn(Text("Hora", color=ft.colors.BLACK, size=12)),
        DataColumn(Text("       Materia", color=ft.colors.BLACK, size=12)),
        DataColumn(Text("Salon", color=ft.colors.BLACK, size=12))
    ]

    # Crear las filas del DataTable
    rows = [
        DataRow(
            cells=[
                DataCell(Container(content=Text(time.replace("-", ""), color=ft.colors.BLACK, size=8, height=60), margin=ft.margin.all(9))),  # Hora
                DataCell(Container(content=Text(details.get("materia", ""), color=ft.colors.BLACK, size=7, height=60), margin=ft.margin.all(10))),  # Materia
                DataCell(Container(content=Text(" :EDIFICIO\n".join(details.get("materia_data", "").split(", ")[1:3]), color=ft.colors.BLACK, size=7, height=60), margin=ft.margin.all(10)))  # Materia Data (valores 1 y 2)
            ]
        ) for time, details in day_schedule.items()
    ]

    # Agregar una fila adicional al final
    rows.append(
        DataRow(
            cells=[
                DataCell(Text("")),
                DataCell(Text("")),
                DataCell(Text(""))
            ]
        )
    )

   
    data_table = DataTable(
        width=900,
        columns=columns,  # Asegurar que el DataTable tenga columnas visibles
        rows=rows,
        divider_thickness=1,
        column_spacing=25,  # Aumentar el espaciado entre columnas
        heading_row_color=ft.colors.BLACK12,
        heading_row_height=50,
        data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
        show_checkbox_column=False,
        expand=True  # Asegurar que el DataTable se expanda
    )

    return data_table

def ScheduleView(page: ft.Page):
  
    page.window.width = 390
    page.window.height = 844

    nav_top= create_nav_top(page)

    nav_bar = create_nav_bar(page)

    # Crear el ViewModel
    view_model = ScheduleViewModel()

    # Crear las pestañas para cada día de la semana
    tabs = Tabs(
        tabs=[
            Tab(text="Lunes", content=create_tab_content(view_model.get_day_schedule("Lunes"))),
            Tab(text="Martes", content=create_tab_content(view_model.get_day_schedule("Martes"))),
            Tab(text="Miércoles", content=create_tab_content(view_model.get_day_schedule("Miercoles"))),
            Tab(text="Jueves", content=create_tab_content(view_model.get_day_schedule("Jueves"))),
            Tab(text="Viernes", content=create_tab_content(view_model.get_day_schedule("Viernes"))),
            Tab(text="Sábado", content=create_tab_content(view_model.get_day_schedule("Sábado")))
        ],
        expand=True,
        indicator_color=ft.colors.WHITE,
        label_color=ft.colors.WHITE,
        unselected_label_color=ft.colors.WHITE,
        height=50  
    )

    # Envolver las pestañas en un contenedor con fondo naranja
    tabs_container = Container(
        content=tabs,
        bgcolor="#E68F59",
        border_radius=ft.border_radius.all(10),  # Bordes redondeados
        padding=ft.padding.all(10),
        width=900,
        margin=ft.margin.only(bottom=40),  # Padding opcional
        expand=True  # Asegurar que el contenedor se expanda
    )

    # Crear un contenedor principal que ocupe todo el espacio disponible
    main_container = Container(
        content=ft.Column(
            controls=[nav_top,
                Container(
                    content=Text("Horario", size=24, weight="bold", color=ft.colors.BLACK),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=20 , bottom=30)
                ),
                Container(
                    content=tabs_container,
                    expand=True  # Asegurar que las pestañas se expandan
                ) 
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        expand=True,
        margin=ft.margin.all(0),   
        padding=ft.padding.all(0)   
    )

    page.update()
    return View("/schedule", [main_container],bgcolor="white",padding=0, spacing=0, appbar=nav_bar)
