from dotenv import load_dotenv
import logging
import os

from services.pdf_extractor_service import PDFTextExtractor
from services.summary_service import SummaryGenerator
from services.cards_service import AmveraMemoryCardGenerator
from storage_config import EXTRACT_TEXT_PATH, CARDS_PATH, SUMMARIES_PATH


class DocumentProcessor:

    def __init__(self, token: str, model: str, url: str):
        load_dotenv()
        self.pdf_service = PDFTextExtractor()
        self.summary_service = SummaryGenerator()
        self.cards_service = AmveraMemoryCardGenerator(token, model, url)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    def extract_text(self, pdf_path: str) -> str:
        pages_data = self.pdf_service.process_pdf(pdf_path)

        text = self.pdf_service.pages_data_to_text(pages_data)

        base_filename = self.get_base_filename(pdf_path)
        new_path = EXTRACT_TEXT_PATH+'/'+base_filename
        self.save_to_txt(text, new_path)

        return self.pdf_service.pages_data_to_text(pages_data)

    def generate_summary(self, pdf_path: str) -> str:

        text = self.extract_text(pdf_path)
        summary = self.summary_service.summarize(text)

        base_filename = self.get_base_filename(pdf_path)
        new_path = SUMMARIES_PATH+'/'+base_filename
        self.save_to_txt(summary, new_path)

        return summary

    def generate_cards(self, pdf_path):

        text = self.extract_text(pdf_path)
        cards = self.cards_service.generate_cards(text)

        base_filename = self.get_base_filename(pdf_path)
        new_path = CARDS_PATH+'/'+base_filename
        self.save_to_txt(cards, new_path)

        return cards

    def full_pipeline(self, pdf_path):

        text = self.extract_text(pdf_path)
        summary = self.summary_service.summarize(text)
        cards = self.cards_service.generate_cards(summary)

        return {
            "text": text,
            "summary": summary,
            "cards": cards
        }

    @staticmethod
    def get_base_filename(pdf_path: str) -> str:
        """
        Получаем имя файла без .pdf
        """

        return os.path.splitext(
            os.path.basename(pdf_path)
        )[0]

    def save_to_txt(self, text: str, output_path: str) -> None:
        """
        Сохраняет извлеченный текст в один файл для быстрой проверки.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        self.logger.info(f"Текст сохранен в {output_path}")

    