from __future__ import annotations

from typing import TYPE_CHECKING

from .prompts import MEMORY_CARDS_SYSTEM_MESSAGES

if TYPE_CHECKING:
    from openai import OpenAI
    from openai.types.chat import ChatCompletionMessageParam
    from .states import CardsGenerationState



class MemoryCardsNodes:

    def __init__(
        self,
        llm: OpenAI
    ):
        self._llm = llm

    def generate_cards(
        self,
        state: CardsGenerationState
    ) -> CardsGenerationState:

            messages: list[ChatCompletionMessageParam] = [
                *MEMORY_CARDS_SYSTEM_MESSAGES,
                {
                    "role": "user",
                    "content": state["document_text"]
                }
            ]
            try:


                response = self._llm.chat.completions.create(
                    model="gpt-4.1",
                    messages=messages
                )
                answer_text = response.choices[0].message.content or ""
                return {**state, "answer_text": answer_text, "success": True, "error": None}

            except Exception as e:
                return{
                    **state,
                    "success": False,
                    "error": str(e),
                    "retries": state["retries"] + 1,
                    "document_text": state["document_text"],
                }