from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

class StateModel(BaseModel):
    user_input: str = ""
    preprocessed_input: str = ""
    think_result: str = ""
    act_result: str = ""
    branch: str = ""
    final_output: str = ""


def preprocess_node(state: StateModel) -> dict:
    """
    Preprocess the user input by stripping whitespace and converting to uppercase.
    You may add any additional logic needed.
    """
    processed = state.user_input.strip().upper()
    return {"preprocessed_input": processed}

def think_node(state: StateModel) -> dict:
    """
    "Think": generate a thought based on preprocessed input if available, otherwise use raw input.
    """
    input_text = state.preprocessed_input if state.preprocessed_input else state.user_input
    return {"think_result":
                f"I think that {input_text}"}

def act_node(state: StateModel) -> dict:
    """
    "Act": build on the thought.
    """
    return {"act_result": f"{state.think_result} "
                          f"and I decide to act on it."}

def branch_node(state: StateModel) -> dict:
    """
    "Branch": decide the next path based on act_result.
    """
    if "SPECIAL" in state.act_result.upper():
        return {"branch": "special_observe"}
    return {"branch": "observe"}

def observe_node(state: StateModel) -> dict:
    """
    "Observe": produce a standard final output.
    """
    return {"final_output":
                f"{state.act_result} and I"
                f" observe a normal outcome."}

def special_observe_node(state: StateModel) -> dict:
    """
    "Special Observe": produce an alternative final output.
    """
    return {"final_output": f"{state.act_result} "
                            f"but because it was special, "
                            f"I altered my observation."}

class FlowGraphHelper:
    """
    Multi-step workflow with an additional preprocessing step.
    The full flow is:
        START → preprocess → think →
        act → branch (via brancher) →
        (observe or special_observe) → END.
    """
    def __init__(self):
        self.graph_builder = StateGraph(StateModel)

        self.graph_builder.add_node("preprocess", preprocess_node)
        self.graph_builder.add_node("think", think_node)
        self.graph_builder.add_node("act", act_node)
        self.graph_builder.add_node("brancher", branch_node)
        self.graph_builder.add_node("observe", observe_node)
        self.graph_builder.add_node("special_observe", special_observe_node)

        self.graph_builder.add_edge(START, "preprocess")
        self.graph_builder.add_edge("preprocess", "think")
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

    def invoke_flow(
            self,
            user_input: str,
    ) -> str:
        """
        Invokes the graph with the given user input and returns the final output.
        """
        initial_state = {"user_input": user_input}
        result = self.compiled_graph.invoke(initial_state)
        return result.get(
            "final_output",
            "No output produced",
        )
