from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletionMessageParam


MEMORY_CARDS_SYSTEM_MESSAGES: list[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": "Ты сервис по созданию учебных карточек формата вопрос-ответ."
            " Создай не больше 10 карточек по тексту и напиши ответ в следующем формате json: "
            "question: Текст вопроса."
            "answer: Текст ответа."
    }
]