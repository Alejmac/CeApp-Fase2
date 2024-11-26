import flet as ft
from flet import Page, Column, Text, Container, ElevatedButton, BottomSheet, ScrollMode, View
from View.nav_top_View import create_nav_top
from View.nav_bar_View import create_nav_bar 
from ViewModel.teacher_ViewModel import TeacherViewModel  
import os

def create_data_table(items):

    columns = [
        ft.DataColumn(ft.Text("Campo", color=ft.colors.BLACK)),
        ft.DataColumn(ft.Text("__________________________________", color=ft.colors.BLACK))
    ]

    rows = []
    for materia in items['materias']:
        rows.extend([
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Clave", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['clave'], color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Nombre", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['nombre'], color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("División", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['division'], color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Grupo", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['grupo'], color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Tipo", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['tipo'], color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Tipo Ponderación", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['tipo_pond'], color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Primer Parcial", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['primer_parcial'] or '', color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Segundo Parcial", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['segundo_parcial'] or '', color=ft.colors.BLACK))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Tercer Parcial", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(materia['tercer_parcial'] or '', color=ft.colors.BLACK))
                ]
            )
        ])


    data_table = ft.DataTable(
        columns=columns,
        rows=rows,
        divider_thickness=1,  # Línea divisoria en medio
        column_spacing=10,
        heading_row_color="#E68F59",
        heading_row_height=50,
        data_row_color={ft.ControlState.HOVERED: "white"},
        show_checkbox_column=False,
    )

    return data_table

def show_bottom_sheet(page, items):
    bottom_sheet_content = Column(
        controls=[
            create_data_table(items)
        ],
        spacing=10,
        scroll=ScrollMode.ALWAYS  
    )

    bottom_sheet_container = Container(
        content=bottom_sheet_content,
        height=900,  
        bgcolor=ft.colors.WHITE,  # Cambiar el color de fondo a blanco
        
    )

    # Crear el BottomSheet
    bottom_sheet = BottomSheet(
        content=bottom_sheet_container,
        open=True,
        on_dismiss=lambda e: print("BottomSheet cerrado")
    )

    # Agregar el BottomSheet a la página
    page.overlay.append(bottom_sheet)
    page.update()

def TeachersView(page: ft.Page):
    page.window.width = 390
    page.window.height = 844

    nav_top = create_nav_top(page)
    
    nav_bar = create_nav_bar(page)
    nav_bar.width = page.window.width 

    # Obtener los datos de los profesores desde el ViewModel
    view_model = TeacherViewModel()
    datos_profesores = view_model.get_teachers()
    print("Datos de los profesores en TeachersView:", datos_profesores)  # Agregar declaración de impresión

    # Crear los botones para cada materia
    buttons = []
    
    for profesor, items in datos_profesores.items():
        for materia in items['materias']:
            print(f"Creando botón para materia: {materia['nombre']} del profesor: {profesor}")  # Agregar declaración de impresión
            buttons.append(
                ElevatedButton(
                    text=materia['nombre'],
                    on_click=lambda e, profesor=profesor, items=items: show_bottom_sheet(page, items),
                    style=ft.ButtonStyle(
                        bgcolor='#b8d1e7',
                        color=ft.colors.BLACK,
                        padding=ft.padding.all(15),
                        elevation=10,
                        text_style=ft.TextStyle(
                            size=8,  
                        )
                    ),
                    width=250,  
                    height=50,  
                )
            )

    # Crear un Column con los botones
    button_column = Column(
        controls=buttons,
        alignment=ft.MainAxisAlignment.CENTER,  # Centrar los botones verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar los botones horizontalmente
        scroll=ScrollMode.ALWAYS  # Habilitar el scroll
    )

    # Crear un Container para centrar el Column con los botones
    button_container = Container(
        content=button_column,
        alignment=ft.alignment.center,  # Centrar el Container
        margin=ft.margin.only(top=0, left=13 , bottom= 40)  # Separación de 20 px arriba y 10 px a la izquierda
    )

    # Crear un título "Materias"
    title_container = Container(
        content=Text(
            "Materias",
            size=30,
            weight="bold",
            color=ft.colors.BLACK,
            font_family="DM Serif Display", 
        ),
        alignment=ft.alignment.center,  # Centrar el título
        margin=ft.margin.only(top=10, bottom=0)  # Margen superior de 30 px y sin margen inferior
    )
    nav_top = create_nav_top(page)    
    # Crear un contenedor principal que ocupe todo el espacio disponible
    main_container = Container(
        content=ft.Column(
            controls=[
                # Crear la barra de navegación superior
                nav_top,
                title_container,  # Agregar el título
                button_container
                   
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        expand=True,
        margin=ft.margin.only(bottom=10), 
        padding=ft.padding.all(0)  
        
    )
    page.update()
    return View("/teachers", [main_container], bgcolor="#f5f5f5", padding=0, spacing=0, appbar=nav_bar)
 