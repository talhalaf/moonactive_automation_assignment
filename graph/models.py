from __future__ import annotations

from typing import List, Literal, Dict, Any, Optional

from pydantic import BaseModel, Field



Difficulty = Literal["easy", "medium", "hard"]

class LevelConfig(BaseModel):
    level: int = Field(ge=1, description="Game level number (>=1)")
    difficulty: Difficulty
    reward: int = Field(ge=0, description="Reward >= 0")
    time_limit: int = Field(gt=0, description="Time limit in seconds (>0)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "level": 3,
                    "difficulty": "medium",
                    "reward": 150,
                    "time_limit": 90,
                }
            ]
        }
    }


class ValidationResult(BaseModel):
    valid: bool
    errors: List[str]

class LLMFeedback(BaseModel):
    analysis: str = Field(default="", description="Analysis of the input configuration")
    suggested_actions: List[str] = Field(default_factory=list, description="List of 0 to 3 suggested actions based on the analysis")


class ValidateResponse(BaseModel):
    schema_validation: ValidationResult
    llm_feedback: LLMFeedback

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "schema_validation": {"valid": True, "errors": []},
                    "llm_feedback": {"analysis": "", "suggested_actions": []},
                }
            ]
        }
    }
