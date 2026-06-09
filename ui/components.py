import flet as ft


def create_title():
    return ft.Text(
        "PDF2Cards",
        size=28,
        weight=ft.FontWeight.BOLD
    )


def create_result_field():
    return ft.TextField(
        label="Результат",
        multiline=True,
        min_lines=20,
        max_lines=30,
        expand=True,
        read_only=True
    )


def create_file_label():
    return ft.Text(
        "Файл не выбран"
    )