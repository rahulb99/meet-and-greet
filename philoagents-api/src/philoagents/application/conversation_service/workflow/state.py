from langgraph.graph import MessagesState


class CelebState(MessagesState):
    """State class for the LangGraph workflow. It keeps track of the information necessary to maintain a coherent
    conversation between the Celeb and the user.

    Attributes:
        celeb_context (str): The historical context of the celeb.
        celeb_name (str): The name of the celeb.
        celeb_perspective (str): The perspective of the celeb about AI.
        celeb_style (str): The style of the celeb.
        summary (str): A summary of the conversation. This is used to reduce the token usage of the model.
    """

    celeb_context: str
    celeb_name: str
    celeb_perspective: str
    celeb_style: str
    summary: str


def state_to_str(state: CelebState) -> str:
    if "summary" in state and bool(state["summary"]):
        conversation = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    else:
        conversation = ""

    return f"""
CelebState(celeb_context={state["celeb_context"]}, 
celeb_name={state["celeb_name"]}, 
celeb_perspective={state["celeb_perspective"]}, 
celeb_style={state["celeb_style"]}, 
conversation={conversation})
        """
