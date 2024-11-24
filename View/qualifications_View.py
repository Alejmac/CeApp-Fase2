import flet as ft
from flet import Page, Column, Text, Container, ScrollMode, icons, AlertDialog, DataTable, DataColumn, DataRow, DataCell, View
from View.nav_top_View import create_nav_top
from View.nav_bar_View import create_nav_bar  
from ViewModel.quialifications_ViewModel import QualificationsViewModel  
import os

def create_collection_container(materia, primer_parcial, segundo_parcial, tercer_parcial, collection, index):
    subtitle = Text(f"{materia}", size=9, weight="bold", color=ft.colors.BLACK)   

    
    subcontainers = [
        Container(
            content=Text(f"{primer_parcial}", size=10,color=ft.colors.BLACK),  # Mostrar solo el valor
            padding=ft.padding.all(15),   
            bgcolor=ft.colors.WHITE,   
            alignment=ft.alignment.center,   
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(bottom=18),
            border=ft.border.all(1, "#1A74AF")
    
        ),
        Container(
            content=Text(f"{segundo_parcial}", size=10,color=ft.colors.BLACK),  # Mostrar solo el valor
            padding=ft.padding.all(15),  # Hacer el triple de grande
            bgcolor=ft.colors.WHITE,  # Fondo blanco
            alignment=ft.alignment.center,  # Centrar el contenido
            border_radius=ft.border_radius.all(8),  # Redondeo de 8px
            margin=ft.margin.only(bottom=18) ,
            border=ft.border.all(1, "#1A74AF")

        ),
        Container(
            content=Text(f"{tercer_parcial}", size=10,color=ft.colors.BLACK),  # Mostrar solo el valor
            padding=ft.padding.all(15),   
            bgcolor=ft.colors.WHITE,  
            alignment=ft.alignment.center,   
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(bottom=18),
            border=ft.border.all(1, "#1A74AF")
        ),        
        Container(
            content=Text(f"suma", size=10,color=ft.colors.BLACK),  # Mostrar solo el valor
            padding=ft.padding.all(15),   
            bgcolor=ft.colors.WHITE,  
            alignment=ft.alignment.center,   
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(bottom=18),
            border=ft.border.all(2,ft.colors.ORANGE)
        )
    ]

    # Determinar el color de fondo del contenedor principal
    #bgcolor ='#E68F59' if index % 2 == 0 else "#1A74AF"
    bgcolor = ft.colors.WHITE

    collection_container = Container(
        content=ft.Column(
            controls=[
                Container(
                    content=ft.Row(
                        controls=[subtitle],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    alignment=ft.alignment.center,  
                    border_radius=ft.border_radius.all(8),
                    height=70,  
                    margin=ft.margin.only(left=10, right=10,) 
                ),
                ft.Row(  # Colocar los contenedores horizontalmente
                    controls=subcontainers,
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrar los subcontenedores
                    spacing=4,  # Sin separación entre los subcontenedores
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0   
        ),
        padding=ft.padding.all(0),   
        border=ft.border.all(0.5, ft.colors.GREY),
        border_radius=ft.border_radius.all(20),  
        margin=ft.Margin(left=30, top=0, right=30, bottom=8),   
        bgcolor=bgcolor,
             
    )

    return collection_container

def QualificationsView(page: Page):
    page.spacing = 0
    page.padding = 0
    
    
    page.window.width = 390
    page.window.height = 844

    nav_top = create_nav_top(page)
    
    
    view_model = QualificationsViewModel()
    materias = view_model.get_materias()
    primer_parcial = view_model.get_primer_parcial()
    segundo_parcial = view_model.get_segundo_parcial()
    tercer_parcial = view_model.get_tercer_parcial()
    schedule = view_model.get_schedule()

    # Crear los contenedores para cada colección de calificaciones, omitiendo el ultimo
    collection_containers = [
        create_collection_container(materias[i], primer_parcial[i], segundo_parcial[i], tercer_parcial[i], schedule.get(materias[i], {}), i)
        for i in range(len(materias) - 1)
    ]

    # Crear un Column con los contenedores de las colecciones
    collection_column = Column(
        controls=collection_containers,
        expand=True,
        alignment=ft.MainAxisAlignment.START,  # Alinear los contenedores al inicio
        scroll=ScrollMode.ALWAYS,  # Habilitar el scroll
        spacing=0  # Sin separación entre los contenedores
    )

    # Crear un contenedor principal que ocupe todo el espacio disponible
    main_container = Container(
        content=ft.Column(
            controls=[
                nav_top,
                Container(
                    content=Text("Calificaciones", size=24, weight="bold", color=ft.colors.BLACK),  # Título principal con estilo
                    alignment=ft.alignment.center, 
                    padding=ft.padding.all(10),   
                    margin=ft.margin.only( top=20 , bottom=20)   
                ),
                collection_column  # Agregar el Column con los contenedores de las colecciones
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0   
        ),
        expand=True,
        margin=ft.margin.only(top=0),   
        padding=ft.padding.all(0)   
    )
 
    page.update()
    return View("/qualifications", [main_container], bgcolor="#f5f5f5", padding=0, spacing=0, appbar=create_nav_bar(page))
