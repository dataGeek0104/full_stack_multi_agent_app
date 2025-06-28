from typing import Any, TypedDict


class FinalDispatch(TypedDict):
    answer: str
    tool: str


class AgentState(TypedDict):
    agent_type: str
    input: str
    intermediate_steps: list[tuple[str, Any]]
    decision_output: Any
    routing_output: Any
    web_results: str
    output: str
    dispatched_output: FinalDispatch


class CustomAgentAction(TypedDict):
    tool: str
    thought: str
