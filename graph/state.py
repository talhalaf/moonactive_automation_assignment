from typing import Dict, TypedDict, Any
from pydantic import BaseModel, Field

from graph.models import LLMFeedback, LevelConfig


class SchemaValidationState(TypedDict):
    schema_validation: Dict[str, object]

class LLMFeedbackState(TypedDict):
    llm_feedback: Dict[str, object]

class InputState(TypedDict):
    input_config: LevelConfig

class OutputState(TypedDict):
    schema_validation: SchemaValidationState
    llm_feedback: LLMFeedbackState

class OverallState(TypedDict):
    """Graph state schema (Pydantic).
    input_config: LevelConfig
    schema_validation: SchemaValidationState
    llm_feedback: LLMFeedback
    """

    input_config: LevelConfig
    schema_validation: SchemaValidationState
    llm_feedback: LLMFeedbackState