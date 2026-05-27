from typing import Protocol, NamedTuple

class CardQuestion(NamedTuple):
    text: str
    answer: str

class MemoryCardGenerator(Protocol):
    '''
    api для работы с моделью
    '''
    def generate_cards(self, text: str) -> str: ...