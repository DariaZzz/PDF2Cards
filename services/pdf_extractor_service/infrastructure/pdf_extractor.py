import pdfplumber
import os
from typing import List, Dict
import logging

from services.pdf_extractor_service.core.adapters.pdf_extractor import PDFExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFTextExtractor(PDFExtractor):
    def __init__(self, ocr_model=None):
        """
        Инициализация экстрактора.
        В будущем здесь можно инициализировать OCR модель (например, PaddleOCR),
        если мы хотим поддерживать ленивую загрузку.
        """
        self.ocr_model = ocr_model

    def extract_text_from_page(self, page) -> str:
        """
        Извлекает текст с одной страницы pdfplumber.
        Пытается сохранить читаемость, объединяя строки.
        """
        # extract_text() возвращает весь текст страницы одной строкой
        # Мы можем настроить параметры, например, x_tolerance и y_tolerance,
        # чтобы лучше объединять слова, которые визуально близки.
        text = page.extract_text(x_tolerance=3, y_tolerance=3)

        if not text:
            return ""

        # Очистка от лишних пустых строк и нормализация пробелов
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return "\n".join(lines)

    def process_pdf(self, file_path: str) -> List[Dict]:
        """
        Основная функция. Принимает путь к PDF, возвращает список словарей.
        Каждый словарь: {'page_num': int, 'text': str}

        Это важно для будущего чанкинга, чтобы знать, откуда взялся текст.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        logger.info(f"Начинаю обработку файла: {file_path}")
        pages_data = []

        try:
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)
                logger.info(f"Всего страниц: {total_pages}")

                for i, page in enumerate(pdf.pages):
                    # 1. Извлекаем текст
                    text = self.extract_text_from_page(page)

                    # 2. Простая эвристика: если текста очень мало, возможно это скан или пустая страница
                    # Для полноценного OCR тут нужно подключить PaddleOCR/Tesseract
                    if len(text) < 50:
                        logger.warning(
                            f"Страница {i + 1} содержит мало текста ({len(text)} символов). Возможно, требуется OCR.")
                        # Здесь будет вызов self._run_ocr(page.image) в полной версии

                    if text:
                        pages_data.append({
                            "page_num": i + 1,
                            "text": text
                        })

        except Exception as e:
            logger.error(f"Ошибка при чтении PDF: {e}")
            raise e

        logger.info(f"Успешно извлечен текст с {len(pages_data)} страниц.")
        return pages_data

    def save_to_txt(self, pages_data: list[dict], output_path: str) -> None:
        """
        Сохраняет извлеченный текст в один файл для быстрой проверки.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for page in pages_data:
                f.write(f"\n--- PAGE {page['page_num']} ---\n")
                f.write(page['text'])
                f.write("\n")
        logger.info(f"Текст сохранен в {output_path}")


    def pages_data_to_text(self, pages_data: list[dict]) -> str:
        result = ""
        for page in pages_data:
            result += page["text"]
            result += "\n"
        return result

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 200) -> list[str]:
        """Простое разбиение по словам с сохранением границ абзацев"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_len = 0

        for word in words:
            current_chunk.append(word)
            current_len += 1
            if current_len >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_len = 0

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks