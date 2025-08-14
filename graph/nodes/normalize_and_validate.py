from typing import List

from pydantic import ValidationError
from graph.models import LevelConfig, ValidationResult
from graph.state import OverallState


def normalize_and_validate_node(state):
    """
    Validate input_config against LevelConfig model.

    Returns schema_validation = { valid: bool, errors: list[str] }.
    """
    config = state.get("input_config", {})
    errors: List[str] = []
    try:
        # This performs full Pydantic validation and coercion if applicable
        LevelConfig.model_validate(config)
        return {"schema_validation": ValidationResult(valid=True, errors=[]).model_dump()}
    except ValidationError as ve:
        # Flatten error messages into human-readable strings
        for err in ve.errors():
            loc = ".".join(str(p) for p in err.get("loc", []))
            msg = err.get("msg", "Invalid value")
            errors.append(f"{loc}: {msg}" if loc else msg)
        return {"schema_validation": ValidationResult(valid=False, errors=errors).model_dump()}