from dotenv import load_dotenv

from services.pdf_extractor_service import PDFTextExtractor
from services.summary_service import SummaryGenerator
from services.cards_service import AmveraMemoryCardGenerator


class DocumentProcessor:

    def __init__(self, token: str, model: str, url: str):
        load_dotenv()
        self.pdf_service = PDFTextExtractor()
        self.summary_service = SummaryGenerator()
        self.cards_service = AmveraMemoryCardGenerator(token, model, url)

    def extract_text(self, pdf_path: str) -> str:
        pages_data = self.pdf_service.process_pdf(pdf_path)

        return self.pdf_service.pages_data_to_text(pages_data)

    def generate_summary(self, pdf_path: str) -> str:

        text = self.extract_text(pdf_path)
        summary = self.summary_service.summarize(text)

        return summary

    def generate_cards(self, pdf_path):

        text = self.extract_text(pdf_path)
        cards = self.cards_service.generate_cards(text)

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

    