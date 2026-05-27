from typing import NamedTuple

class MemoryCard(NamedTuple):
    '''
    Карточка с вопросом и ответом
    '''
    question: str
    answer: str