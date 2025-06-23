import json
from dataclasses import dataclass

from .agentstates import AgentState, FinalDispatch
from .customchains import SimpleLLMChain
from .customtools import WebSearchTool
from .prompts import decision_prompt, general_answer_prompt, routing_prompt

from langgraph.graph import END, START, StateGraph  # type: ignore[import-not-found]  # isort: skip
from langgraph.graph.state import CompiledStateGraph  # type: ignore[import-not-found]  # isort: skip


@dataclass
class DecisionOutput:
    tool: str
    reasoning: str


@dataclass
class PlanStep:
    tool: str
    input: str
    topic: str


@dataclass
class RoutingOutput:
    step: PlanStep


class FinancialAgent:
    def __init__(self):
        self.model_provider = "google-genai"

    def decision_chain(self, state: AgentState) -> AgentState:
        chain = SimpleLLMChain(
            model_provider=self.model_provider, sys_prompt=decision_prompt
        )
        raw = chain.invoke(question=state["input"])
        json_start = raw.find("{")
        if json_start == -1:
            raise ValueError(f"decision_chain did not return JSON: {raw!r}")
        payload = raw[json_start:].replace("```json", "").replace("```", "").strip()
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from decision_chain: {payload!r}") from e
        decision = DecisionOutput(
            tool=parsed.get("tool", "general"),
            reasoning=parsed.get("reasoning", ""),
        )
        state["decision_output"] = decision
        state["intermediate_steps"].append(("decision_chain", decision))
        print(
            f"INFO  [multi-agent] Decision > Tools: {decision.tool}, Resoning: {decision.reasoning}"
        )
        return state

    def routing_chain(self, state: AgentState) -> AgentState:
        decision: DecisionOutput = state["decision_output"]
        if not decision:
            raise ValueError("routing_chain called without decision_output")
        chain = SimpleLLMChain(
            model_provider=self.model_provider, sys_prompt=routing_prompt
        )
        context = (
            f"Question: {state['input']}\n"
            f"Decision: {json.dumps({'tool': decision.tool, 'reasoning': decision.reasoning})}"
        )
        raw = chain.invoke(question=context)
        raw_json = json.loads(raw.replace("```json", "").replace("```", "").strip())
        step = PlanStep(tool="", input="", topic="")
        if "tool" in raw_json and "input" in raw_json and "topic" in raw_json:
            tool = raw_json["tool"]
            inp = raw_json["input"]
            topic = raw_json["topic"]
            step = PlanStep(tool=tool, input=inp, topic=topic)
        routing = RoutingOutput(step=step)
        state["routing_output"] = routing
        state["intermediate_steps"].append(("routing_chain", routing))
        print(f"INFO  [multi-agent] Routing > Step: {routing.step}")
        return state

    def worker_dispatch(self, state: AgentState) -> AgentState:
        if not state.get("routing_output"):
            raise ValueError("worker_dispatch called without routing_output")
        final_dispatch: FinalDispatch = {"answer": "", "tool": ""}
        final_dispatch["tool"] = state["routing_output"].step.tool
        state["input"] = state["routing_output"].step.input
        if state["routing_output"].step.tool == "general":
            out_state = self.general_answer(state)
            final_dispatch["answer"] = out_state["output"]
        elif state["routing_output"].step.tool == "web_search":
            out_state = self.web_search(state)
            final_dispatch["answer"] = out_state["web_results"]
        state["dispatched_output"] = final_dispatch
        return state

    def general_answer(self, state: AgentState) -> AgentState:
        chain = SimpleLLMChain(
            model_provider=self.model_provider, sys_prompt=general_answer_prompt
        )
        response = chain.invoke(question=state["input"])
        state["intermediate_steps"].append(
            ("general", state["decision_output"].reasoning)
        )
        state["output"] = response
        return state

    def web_search(self, state: AgentState) -> AgentState:
        topic = state["routing_output"].step.topic
        search_tool = WebSearchTool(topic=topic)
        chain = SimpleLLMChain(
            model_provider=self.model_provider, sys_prompt=general_answer_prompt
        )
        chain.llm.bind_tools(tools=[search_tool.as_tool()])
        response = chain.invoke(question=state["input"])
        state["intermediate_steps"].append(
            ("web_search", state["decision_output"].reasoning)
        )
        state["web_results"] = response
        return state

    def build_agent_graph(self) -> CompiledStateGraph:
        graph = StateGraph(AgentState)

        # Main linear flow: Decision → Routing → Dispatch → End
        graph.add_node("decision", self.decision_chain)
        graph.add_node("routing", self.routing_chain)
        graph.add_node("dispatch", self.worker_dispatch)
        # graph.add_node("end", lambda s: s, ["dispatch"], is_terminal=True)
        graph.add_edge(START, "decision")
        graph.add_edge("decision", "routing")
        graph.add_edge("routing", "dispatch")
        graph.add_edge("dispatch", END)

        compiled_graph = graph.compile()

        return compiled_graph
