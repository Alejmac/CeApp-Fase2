import flet as ft
from flet import Page, View, Container, Text
import json
import os

def LoadingView(page: Page):
    with open(os.path.join("Data", "active.json"), "r") as file:
        data = json.load(file)

    if data.get("active", False):
        print("Redirecting to /average")
        page.go("/average")
    else:
        print("Redirecting to /first")
        page.go("/first")

    page.update()

    main_container = Container(content=Text("Loading..."))

    return View("/loading", [main_container], bgcolor="white", padding=0, spacing=0)

