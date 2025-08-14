from dotenv import load_dotenv

from graph.models import LevelConfig
from graph.state import InputState

load_dotenv()

from graph.graph import build_graph



if __name__ == "__main__":

    graph = build_graph()
    # Create an OverallState object with the input_config

    input_config = InputState(input_config=LevelConfig(
        level=154,
        time_limit=10,
        reward=6600,
        difficulty="hard"
    ))

    # Invoke the graph with the OverallState object
    result = graph.invoke(input=input_config)

    print(result)
    print("Schema Validation:", result.get("schema_validation"))
    print("LLM Feedback:", result.get("llm_feedback"))