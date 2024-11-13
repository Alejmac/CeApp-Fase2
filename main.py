import flet as ft
from flet import Page, View, AppBar, ElevatedButton, Text, colors
from View.schedule import ScheduleView
from View.teachers_View import TeachersView
from View.qualifications_View import QualificationsView
from View.data_student_View import DataStudentView
from View.first import FirstView
from View.login_View import LoginView


def main(page: Page):
    page.title = "CeApp"
 
    def route_change(route):
        page.views.clear()
 
        routes = {

            "/schedule": lambda: ScheduleView(page),
            "/teachers": lambda: TeachersView(page),
            "/qualifications": lambda: QualificationsView(page),
            "/data_student": lambda: DataStudentView(page),
            "/login": lambda: LoginView(page),
            "/first": lambda: FirstView(page)
        }
        
        view_function = routes.get(page.route, routes["/first"])
        page.views.append(view_function())   
 
        page.update()
 
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)