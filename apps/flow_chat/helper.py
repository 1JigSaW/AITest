from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

class StateModel(BaseModel):
    user_input: str = ""
    think_result: str = ""
    act_result: str = ""
    branch: str = ""
    final_output: str = ""

def think_node(state: StateModel) -> dict:
    return {"think_result": f"I think that {state.user_input}"}

def act_node(state: StateModel) -> dict:
    return {"act_result": f"{state.think_result} and I decide to act on it."}

def branch_node(state: StateModel) -> dict:
    if "special" in state.act_result.lower():
        return {"branch": "special_observe"}
    return {"branch": "observe"}

def observe_node(state: StateModel) -> dict:
    return {"final_output": f"{state.act_result} and I observe a normal outcome."}

def special_observe_node(state: StateModel) -> dict:
    return {"final_output": f"{state.act_result} but because it was special, I altered my observation."}

class FlowGraphHelper:
    """
    FlowGraphLogic encapsulates the building and invocation of a multi-step workflow
    (simulating a ReAct loop: Think → Act → Branch → Observe) using LangGraph's StateGraph.
    """
    def __init__(self):
        self.graph_builder = StateGraph(StateModel)

        self.graph_builder.add_node("think", think_node)
        self.graph_builder.add_node("act", act_node)

        self.graph_builder.add_node("brancher", branch_node)
        self.graph_builder.add_node("observe", observe_node)
        self.graph_builder.add_node("special_observe", special_observe_node)

        self.graph_builder.add_edge(START, "think")
        self.graph_builder.add_edge("think", "act")
        self.graph_builder.add_edge("act", "brancher")

        self.graph_builder.add_conditional_edges(
            "brancher",
            lambda s: getattr(s, "branch", "observe"),
            {"observe": "observe", "special_observe": "special_observe"}
        )
        self.graph_builder.add_edge("observe", END)
        self.graph_builder.add_edge("special_observe", END)

        self.compiled_graph = self.graph_builder.compile()

    def invoke_flow(self, user_input: str) -> str:
        """
        Invokes the graph with the given user input and returns the final output.
        """
        initial_state = {"user_input": user_input}
        result = self.compiled_graph.invoke(initial_state)
        return result.get("final_output", "No output produced")
