from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

from graph.models import LLMFeedback
from pathlib import Path

llm = ChatOpenAI(
    model="gpt-4o-mini"
)

# llm = ChatAnthropic(
#     model="claude-3-haiku-20240307",
#     temperature=0,
#     max_tokens=1024,
#     timeout=None,
#     max_retries=2
# )

structured_output_llm = llm.with_structured_output(LLMFeedback)

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "graph" / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "llm_review_system.md"
USER_PROMPT_PATH = PROMPTS_DIR / "llm_review_user.md"

def _build_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()

def _build_user_prompt() -> str:
    return USER_PROMPT_PATH.read_text(encoding="utf-8").strip()

system = _build_system_prompt()
user = _build_user_prompt()

llm_feedback_prompt = ChatPromptTemplate(
    messages=[
        ("system", system),
        ("user", user)
    ]
)

llm_feedback_chain = llm_feedback_prompt | structured_output_llm