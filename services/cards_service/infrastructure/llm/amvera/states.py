from typing import TypedDict


class CardsGenerationState(TypedDict):
    document_text: str
    answer_text: str
    retries: int
    success: bool
    error: str | None