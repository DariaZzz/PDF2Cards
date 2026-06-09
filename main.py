import flet as ft
import os
from dotenv import load_dotenv

from services.cards_service.errors import NoTokenError, NoModelError, NoUrlError
from ui.main_page import MainPage


def main(page: ft.Page):
    load_dotenv()

    token = os.getenv("AMVERA_API_TOKEN")
    if token is None:
        raise NoTokenError

    model = os.getenv("LLM_MODEL")
    if model is None:
        raise NoModelError

    url = os.getenv("AMVERA_API_URL")
    if url is None:
        raise NoUrlError

    app = MainPage(page, token, model, url)

    app.build()


ft.run(
    main
)

# import flet as ft
#
# def main(page: ft.Page):
#     page.add(ft.Text("OK"))
#
# ft.run(main, view=ft.AppView.WEB_BROWSER)