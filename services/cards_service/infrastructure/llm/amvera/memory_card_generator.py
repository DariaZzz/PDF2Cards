from __future__ import annotations
from typing import TYPE_CHECKING, cast
import re
from openai import OpenAI


from services.cards_service.core.adapters.memory_card_generator import MemoryCardGenerator, CardQuestion
from services.cards_service.errors import FailedToGenerateCardsError, NoTokenError, NoModelError, NoUrlError
from .nodes import MemoryCardsNodes
from .graph import build_graph

if TYPE_CHECKING:
    from .states import CardsGenerationState


_INITIAL_STATE: CardsGenerationState = {
    "document_text": "",
    "answer_text": "",
    "retries": 0,
    "success": False,
    "error": None,
}


class AmveraMemoryCardGenerator(MemoryCardGenerator):

    def __init__(self, token:str, model:str, url: str) -> None:

        if not token:
            raise NoTokenError("Не указан токен")
        if not model:
            raise NoModelError("Не указана модель")
        if not url:
            raise NoUrlError("Не указан url")


        llm = OpenAI(base_url=url,api_key=token)

        self._graph = build_graph(MemoryCardsNodes(llm=llm))

    def generate_cards(
        self,
        text: str
    ) -> str:


        result = self._graph.invoke({

            "document_text": text,

            "answer_text": "",

            "retries": 0,

            "success": False,

            "error": None
        })

        if result['error']:
            raise FailedToGenerateCardsError
        # result = self.parse_answer(result['answer_text'])

        return result['answer_text']

    def parse_answer(self, answer_text: str) -> list[CardQuestion]:
        questions = re.findall(r'question:\s*START\s*(.*?)\s*END', answer_text)
        answers = re.findall(r'answer:\s*START\s*(.*?)\s*END', answer_text)
        result = []
        for question, answer in zip(questions, answers):
            result.append(CardQuestion(text=question, answer=answer))
        return result
