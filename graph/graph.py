"""LangGraph graph for Configuration Validation.

Linear graph:
- normalize_and_validate: Pydantic validation
- llm_review: returns LLM feedback
- assemble_response: merges outputs

Inputs: input_config (dict)
Outputs: schema_validation, llm_feedback

Errors: Pydantic errors captured in schema_validation; no exceptions raised.
"""
from langgraph.graph import END, START, StateGraph

from .state import (
    InputState,
    OutputState,
    OverallState
)

from .consts import (
    NORMALIZE_AND_VALIDATE,
    LLM_REVIEW,
    ASSEMBLE_RESPONSE,
)

from .nodes.normalize_and_validate import normalize_and_validate_node
from .nodes.llm_review import llm_review_node
from .nodes.assemble_response import assemble_response_node

# if schema is valid, go to LLM_REVIEW
def should_continue(state: OverallState):
    return LLM_REVIEW if state.get("schema_validation", {}).get("valid", False) else END

def build_graph():
    """
    Build and return the compiled LangGraph for validation flow.

    START -> normalize_and_validate -> llm_review -> assemble_response -> END
    """
    graph = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

    graph.add_node(NORMALIZE_AND_VALIDATE, normalize_and_validate_node)
    graph.add_node(LLM_REVIEW, llm_review_node)
    graph.add_node(ASSEMBLE_RESPONSE, assemble_response_node)

    graph.add_edge(START, NORMALIZE_AND_VALIDATE)
    graph.add_conditional_edges(NORMALIZE_AND_VALIDATE, should_continue, [LLM_REVIEW, END])
    graph.add_edge(LLM_REVIEW, ASSEMBLE_RESPONSE)
    graph.add_edge(ASSEMBLE_RESPONSE, END)

    return graph.compile()

