import os
import logging

from dotenv import load_dotenv

from services.pdf_extractor_service.infrastructure.pdf_extractor import PDFTextExtractor
from services.summary_service.infrastructure.summary_generator import SummaryGenerator
from services.cards_service.infrastructure.llm.amvera.memory_card_generator import AmveraMemoryCardGenerator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_to_txt(text: str, filename: str):
    """
    Сохраняет текст в txt файл
    """

    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    logger.info(f"Файл сохранён: {path}")


def get_base_filename(pdf_path: str) -> str:
    """
    Получаем имя файла без .pdf
    """

    return os.path.splitext(
        os.path.basename(pdf_path)
    )[0]


def main():

    logger.info("Запуск PDF2Cards")

    # --- сервисы ---
    load_dotenv()
    token=os.getenv("AMVERA_API_TOKEN")
    model=os.getenv("LLM_MODEL")
    url=os.getenv("AMVERA_API_URL")
    print("Загрузка суммаризатора")
    summarizer = SummaryGenerator()
    print("Суммаризатор готов")
    memory_card_generator = AmveraMemoryCardGenerator(token,model,url)
    text_extractor = PDFTextExtractor()


    while True:

        print("\n==============================")
        print("PDF2Cards")
        print("==============================\n")

        pdf_path = input(
            "Введите путь до PDF файла "
            "(или 'exit' для выхода): "
        ).strip()

        if pdf_path.lower() == "exit":
            print("Выход...")
            break

        if not os.path.exists(pdf_path):
            print("Файл не найден.\n")
            continue

        print("\nВыберите действие:")
        print("1 - Извлечь текст")
        print("2 - Сгенерировать конспект")
        print("3 - Сгенерировать карточки")
        print("4 - Полный pipeline")

        choice = input("\nВведите номер: ").strip()

        try:

            logger.info("Извлекаем текст из PDF...")

            text = text_extractor.process_pdf(pdf_path)
            print(text)
            base_name = get_base_filename(pdf_path)

            # --- сохраняем raw text ---
            raw_text_filename = f"{base_name}_raw.txt"
            text = text_extractor.pages_data_to_text(text)
            save_to_txt(
                text,
                raw_text_filename
            )
        #
            print(
                f"\nИзвлечённый текст сохранён:"
                f" {raw_text_filename}"
            )
        #
        #     # ==========================
        #     # 1. Только текст
        #     # ==========================
            match choice:
                case "1":
                    print("\nГотово.")
                    break
        #
        #     # ==========================
        #     # 2. Суммаризация
        #     # ==========================
                case "2":

                    logger.info(
                        "Генерируем конспект..."
                    )

                    summary = summarizer.summarize(text)

                    summary_filename = (
                        f"{base_name}_summary.txt"
                    )

                    save_to_txt(
                        summary,
                        summary_filename
                    )

                    print(
                        f"\nКонспект сохранён:"
                        f" {summary_filename}"
                    )

        #
        #     # ==========================
        #     # 3. Карточки
        #     # ==========================
                case "3":

                    logger.info(
                        "Генерируем карточки..."
                    )

                    cards = memory_card_generator.generate_cards(text)

                    cards_filename = (
                        f"{base_name}_cards.txt"
                    )

                    save_to_txt(
                        cards,
                        cards_filename
                    )

                    print(
                        f"\nКарточки сохранены:"
                        f" {cards_filename}"
                    )

        #
        #     # ==========================
        #     # 4. Полный pipeline
        #     # ==========================
                case "4":

                    logger.info(
                        "Генерируем конспект..."
                    )

                    summary = summarizer.summarize(text)

                    summary_filename = (
                        f"{base_name}_summary.txt"
                    )

                    save_to_txt(
                        summary,
                        summary_filename
                    )

                    logger.info(
                        "Генерируем карточки..."
                    )

                    cards = memory_card_generator.generate_cards(
                        summary
                    )

                    cards_filename = (
                        f"{base_name}_cards.txt"
                    )

                    save_to_txt(
                        cards,
                        cards_filename
                    )

                    print("\nПолный pipeline завершён.")

                case _:
                    print("\nНеверный выбор.")
        #
        except Exception as e:

            logger.error(
                f"Ошибка во время обработки: {e}"
            )

            print(
                "\nПроизошла ошибка при обработке файла."
            )


if __name__ == "__main__":
    main()