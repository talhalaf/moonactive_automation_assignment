from pathlib import Path
from graph.models import LLMFeedback
from graph.state import OverallState

from ..chains.llm_review import llm_feedback_chain

from ..utils.heuristics_loader import load_and_format_heuristics

PROJECT_ROOT = Path(__file__).resolve().parents[2]

heur_text = load_and_format_heuristics(PROJECT_ROOT)

def llm_review_node(state):
    """
    LLM review node.
    """

    # Extract input_config
    input_config = state.get("input_config", {})
    try:
        llm_feedback = llm_feedback_chain.invoke(
            {
            "level": input_config.level,
            "difficulty": input_config.difficulty,
            "reward": input_config.reward,
            "time_limit": input_config.time_limit,
            "heur_text": heur_text,
            }
        )
    except Exception as e:
        llm_feedback = LLMFeedback(
            analysis=f"LLM review failed: {type(e).__name__}. Returning stub.",
            suggested_actions=["Review config manually against heuristics."],
        )
    return {"llm_feedback": llm_feedback}