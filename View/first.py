import flet as ft
from flet import Page, Image, Container, Stack, Column, Text, IconButton, alignment, colors, FontWeight, TextAlign, MainAxisAlignment, CrossAxisAlignment, padding, margin
import os

# Construir la ruta de la imagen
image_path = os.path.join(os.getcwd(), "assets", "entrada1.png")

def FirstView(page: Page):
    #page.window.width = 390
    #page.window.height = 844
    page.title = "Explora la Nueva App"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = colors.BLACK

    # Verifica si la imagen existe
    if not os.path.exists(image_path):
        print(f"Error: La imagen '{image_path}' no se encuentra.")
    else:
        print(f"Imagen encontrada: {image_path}")

    # Contenedor de la imagen sin degradado
    image_container = Container(
        content=Stack(
            [
                Image(
                    src=image_path,
                    fit=ft.ImageFit.COVER,
                    width=page.window.width,
                    height=page.window.height
                ),
                Container(
                    content=Column(
                        [
                            Container(
                                Text(
                                    "Explora la Nueva App",
                                    size=40,
                                    color=colors.WHITE,
                                    weight=FontWeight.BOLD,
                                    text_align=TextAlign.LEFT
                                ),
                                margin=margin.only(top=100)
                            ),
                            Container(
                                IconButton(
                                    icon=ft.icons.ARROW_FORWARD,
                                    icon_size=30,
                                    icon_color=colors.BLACK,
                                    bgcolor=colors.WHITE,
                                    on_click=lambda _: page.go("/login"),  
                                ),
                                margin=margin.only(top=15),
                                alignment=alignment.center
                            )
                        ],
                        alignment=MainAxisAlignment.START,
                        horizontal_alignment=CrossAxisAlignment.START
                    ),
                    
                    alignment=alignment.top_left,
                    padding=padding.all(20)
                )
            ]
        ),
        expand=True,
        width=page.width,
        height=page.height
    )

    # Añadir el contenedor de la imagen a la página
    page.add(image_container)

    # Devolver el objeto View
    return ft.View(
        "/first",
        [image_container]
    )