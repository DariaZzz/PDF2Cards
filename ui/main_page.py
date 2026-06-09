import flet as ft
import asyncio

from processor import DocumentProcessor

from ui.components import (
    create_title,
    create_result_field,
    create_file_label
)


class MainPage:

    def __init__(self, page: ft.Page, token: str, model: str, url: str):

        self.page = page

        self.processor = DocumentProcessor(token, model, url)

        self.selected_pdf = None

        self.file_label = create_file_label()

        self.result_field = create_result_field()



    # ==========================
    # File Picker
    # ==========================

    async def pick_pdf(self, e):

        files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["pdf"]
        )

        if files:
            self.selected_pdf = files[0].path

            self.file_label.value = files[0].name

            self.page.update()

    # ==========================
    # Извлечь текст
    # ==========================

    async def extract_text(self, e):

        if not self.selected_pdf:

            self.result_field.value = (
                "Сначала выберите PDF"
            )

            self.page.update()

            return

        try:

            text = self.processor.extract_text(
                self.selected_pdf
            )

            self.result_field.value = text

        except Exception as ex:

            self.result_field.value = (
                f"Ошибка:\n{str(ex)}"
            )

        self.page.update()

    # ==========================
    # Конспект
    # ==========================

    async def generate_summary(self, e):

        if not self.selected_pdf:
            self.result_field.value = (
                "Сначала выберите PDF"
            )

            self.page.update()

            return

        try:

            self.result_field.value = (
                "Генерирую конспект..."
            )

            self.page.update()

            summary = await asyncio.to_thread(
                self.processor.generate_summary,
                self.selected_pdf
            )

            self.result_field.value = summary

        except Exception as ex:

            self.result_field.value = (
                f"Ошибка:\n{str(ex)}"
            )

        self.page.update()

    # ==========================
    # Карточки
    # ==========================

    async def generate_cards(self, e):

        if not self.selected_pdf:

            self.result_field.value = (
                "Сначала выберите PDF"
            )

            self.page.update()

            return

        try:

            cards = (
                self.processor.generate_cards(
                    self.selected_pdf
                )
            )

            self.result_field.value = cards

        except Exception as ex:

            self.result_field.value = (
                f"Ошибка:\n{str(ex)}"
            )

        self.page.update()

    # ==========================
    # Построение интерфейса
    # ==========================

    def build(self):

        self.page.title = "PDF2Cards"

        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.center()

        self.page.add(

            ft.Column(

                controls=[

                    create_title(),

                    ft.Divider(),

                    ft.ElevatedButton(
                        "Выбрать PDF",
                        on_click=self.pick_pdf

                    ),

                    self.file_label,

                    ft.Row(

                        controls=[

                            ft.Button(
                                "Извлечь текст",
                                on_click=self.extract_text
                            ),

                            ft.Button(
                                "Конспект",
                                on_click=self.generate_summary
                            ),

                            ft.Button(
                                "Карточки",
                                on_click=self.generate_cards
                            )

                        ]

                    ),

                    self.result_field

                ],

                expand=True

            )

        )