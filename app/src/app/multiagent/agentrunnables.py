from typing import Iterator

from .customagents import Agent


class AgentRunnable:
    def __init__(self):
        self.agent = Agent()

    def run(self, question: str, agent_type: str):
        response = self.agent.build_agent_graph().invoke(
            input={
                "agent_type": agent_type,
                "input": question,
                "intermediate_steps": [],
                "decision_output": None,
                "routing_output": None,
                "web_results": [],
                "output": "",
            },
            stream_mode="values",
        )
        return response["dispatched_output"]

    def stream(self, question: str, agent_type: str) -> Iterator[str]:
        graph = self.agent.build_agent_graph()
        inputs = {
            "agent_type": agent_type,
            "input": question,
            "intermediate_steps": [],
            "decision_output": None,
            "routing_output": None,
            "web_results": [],
            "output": "",
        }
        # Stream individual token messages
        for msg, meta in graph.stream(inputs, stream_mode="messages"):
            # Only emit tokens from the dispatch node (i.e., the final answer)
            if meta.get("langgraph_node") == "dispatch":
                yield msg.content
