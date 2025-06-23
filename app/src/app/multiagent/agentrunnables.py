from .customagents import FinancialAgent


class FinancialRunnable:
    def __init__(self):
        self.agent = FinancialAgent()

    def run(self, question: str):
        response = self.agent.build_agent_graph().invoke(
            input={
                "input": question,
                "intermediate_steps": [],
                "decision_output": None,
                "routing_output": None,
                "results": [],
                "output": "",
            },
            stream_mode="values",
        )
        return response["dispatched_output"]
