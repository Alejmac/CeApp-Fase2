import flet as ft
from flet import Page, Column, Text, Container, ScrollMode, View, PieChart, PieChartSection, TextStyle, FontWeight, BoxShadow, colors
from View.nav_top_View import create_nav_top
from View.nav_bar_View import create_nav_bar
import os
from ViewModel.average_ViewModel import AverageViewModel
from ViewModel.data_student_ViewModel import DataStudentViewModel


def AverageView(page: Page):
    page.spacing = 0
    page.padding = 0

    page.window.width = 390
    page.window.height = 844

    nav_top = create_nav_top(page)
    nav_bar = create_nav_bar(page)

    normal_radius = 50
    hover_radius = 60
    normal_title_style = TextStyle(
        size=16, color=colors.BLACK, weight=FontWeight.BOLD
    )
    hover_title_style = TextStyle(
        size=22,
        color=colors.ORANGE,
        weight=FontWeight.BOLD,
        shadow=BoxShadow(blur_radius=2, color=colors.ORANGE_50),
    )

    def on_chart_event(e):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()

    # Obtener los promedios del ViewModel
    view_model = AverageViewModel()
    promedios = view_model.get_promedios()
    promedio_general = view_model.get_promedio_general()
    
    data_student_view_model = DataStudentViewModel()
    student_name = data_student_view_model.get_name()

    chart = PieChart(
        sections=[
            PieChartSection(
                promedio_general,
                title=f"{promedio_general}%",
                title_style=normal_title_style,
                color=colors.BLUE,
                radius=normal_radius,
            ),
            PieChartSection(
                100 - promedio_general,
                title="",
                title_style=normal_title_style,
                color=colors.GREY,
                radius=normal_radius,
            ),
        ],
        sections_space=0,
        center_space_radius=40,
        on_chart_event=on_chart_event,
        expand=True,
    )

    data_points = [
        ft.LineChartDataPoint(index + 1, promedio)
        for index, promedio in enumerate(promedios)
    ]
    line_chart_data = [
        ft.LineChartData(
            data_points=data_points,
            stroke_width=4,
            color=ft.colors.LIGHT_BLUE,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    line_chart = ft.LineChart(
        data_series=line_chart_data,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE))
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=i*20, label=ft.Text(f"{i*20}", size=14, weight=ft.FontWeight.BOLD))
                for i in range(6)
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=i, label=ft.Text(f"{i}", size=16, weight=ft.FontWeight.BOLD))
                for i in range(1, 9)
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
        min_y=0,
        max_y=100,
        min_x=1,
        max_x=8,
        expand=True,
    )

    # Crear un contenedor principal que ocupe todo el espacio disponible
    main_container = Container(
        content=Column(
            controls=[
                nav_top,
                Container(
                    content=Text(f"👋 HOLA!! {student_name} ", size=15, weight="bold", color=colors.BLACK),   
                    alignment=ft.alignment.center_left, 
                    padding=ft.padding.all(10),   
                    margin=ft.margin.only(top=20, bottom=10)   
                ),
                Container(
                    content=Column(
                        controls=[
                            chart,
                            Text("Promedio General", size=16, weight="bold", color=colors.ORANGE)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10),
                    margin=ft.margin.only(top=10, bottom=20,left=60,right=60),
                    bgcolor=ft.colors.WHITE,
                    border_radius=ft.border_radius.all(24),
                    width=300,  
                    height=300,  
                    shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=10,
                    color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                    offset=ft.Offset(0, 4)
    )
                ),
                Container(
                    content=Text("Promedios", size=24, weight="bold", color=colors.BLACK),  # Título principal con estilo
                    alignment=ft.alignment.center, 
                    padding=ft.padding.all(10),   
                    margin=ft.margin.only(top=10, bottom=20)   
                ),
                Container(
                    content=Column(
                        controls=[
                            Text("Avance Académico", size=20, weight="bold", color=colors.ORANGE),
                            line_chart
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(10),
                    margin=ft.margin.only(top=10, bottom=20,left=30,right=30),
                    bgcolor=ft.colors.WHITE,
                    border_radius=ft.border_radius.all(24),
                    width=600,  # Definir el ancho del contenedor
                    height=300,
                    shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=10,
                    color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                    offset=ft.Offset(0, 4)
    )
                    
                ),
                # Aquí puedes agregar más contenido según sea necesario
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0,
            scroll=ScrollMode.ALWAYS  # Habilitar el scroll
        ),
        expand=True,
        margin=ft.margin.only(top=0),   
        padding=ft.padding.all(0)   
    )

    page.update()
    return View("/average", [main_container], bgcolor="#f5f5f5", padding=0, spacing=0, appbar=nav_bar)