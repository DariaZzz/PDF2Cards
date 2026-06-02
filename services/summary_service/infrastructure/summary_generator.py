import logging
import torch

from models.model_config import MODEL_NAME

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

class SummaryGenerator:

    def __init__(
        self,
        model_name=MODEL_NAME
    ):

        logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.logger.info(f"Используем device: {self.device}")

        # --- tokenizer ---
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # --- model ---
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        ).to(self.device)


    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 200
    ) -> list[str]:

        words = text.split()

        chunks = []
        current_chunk = []

        for word in words:

            current_chunk.append(word)

            if len(current_chunk) >= chunk_size:

                chunks.append(
                    " ".join(current_chunk)
                )

                current_chunk = []

        if current_chunk:
            chunks.append(
                " ".join(current_chunk)
            )

        return chunks

    def summarize_chunk(
        self,
        text_chunk: str
    ) -> str:

        try:

            prompt = "summary | " + text_chunk

            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=1024
            ).to(self.device)

            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=150,
                min_length=40,
                num_beams=4,
                early_stopping=True
            )

            summary = self.tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True
            )

            return summary.strip()

        except Exception as e:

            self.logger.error(
                f"Ошибка при суммаризации: {e}"
            )

            return ""

    def summarize(
        self,
        text: str,
        chunk_size: int = 200
    ) -> str:

        chunks = self.chunk_text(
            text,
            chunk_size
        )

        summaries = []

        self.logger.info(
            f"Разбил текст на {len(chunks)} чанков"
        )

        for i, chunk in enumerate(chunks):

            self.logger.info(
                f"Чанк {i+1}/{len(chunks)}"
            )

            chunk_summary = self.summarize_chunk(
                chunk
            )

            if chunk_summary:
                summaries.append(
                    chunk_summary
                )

        return "\n\n".join(summaries)

    def save_summary_to_txt(
        self,
        summary_text: str,
        output_path: str
    ):

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(summary_text)

        self.logger.info(
            f"Сохранено: {output_path}"
        )


if __name__ == "__main__":
    summary = SummaryGenerator()