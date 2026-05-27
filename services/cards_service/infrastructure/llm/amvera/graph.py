from __future__ import annotations

from langgraph.graph import StateGraph, END

from services.cards_service.infrastructure.llm.amvera.states import CardsGenerationState

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langgraph.graph.state import CompiledStateGraph

    from .nodes import MemoryCardsNodes


MAX_RETRIES = 3
_GENERATE_NODE = "generate_cards"

# условный переход
def should_retry(state: CardsGenerationState) -> str:
    if state["success"] or state["retries"] >= MAX_RETRIES:
        return END
    return _GENERATE_NODE


def build_graph(
    nodes: MemoryCardsNodes
) -> CompiledStateGraph[CardsGenerationState]:

    graph: StateGraph[CardsGenerationState] = StateGraph(CardsGenerationState)

    graph.add_node(_GENERATE_NODE, nodes.generate_cards)
    graph.set_entry_point(_GENERATE_NODE)

    graph.add_conditional_edges(_GENERATE_NODE,should_retry)

    return graph.compile()