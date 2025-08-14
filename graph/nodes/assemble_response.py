from graph.state import OverallState
from graph.models import LLMFeedback, ValidationResult


def assemble_response_node(state):
    """
    Merge current state into final OverallState. No transformation beyond ensuring keys exist.
    """
    
    schema_validation = state.get("schema_validation", {})
    llm_feedback = state.get("llm_feedback", {})
    input_config = state.get("input_config", {})
    
    if not schema_validation:
        schema_validation = ValidationResult(valid=False, errors=["Missing schema_validation"]).model_dump()
    if not llm_feedback:
        llm_feedback = LLMFeedback().model_dump()

    return {
        "input_config": input_config,
        "schema_validation": schema_validation,
        "llm_feedback": llm_feedback,
    }