from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode

from philoagents.application.conversation_service.workflow.chains import (
    get_context_summary_chain,
    get_conversation_summary_chain,
    get_celeb_response_chain,
)
from philoagents.application.conversation_service.workflow.state import CelebState
from philoagents.application.conversation_service.workflow.tools import tools
from philoagents.config import settings

retriever_node = ToolNode(tools)


async def conversation_node(state: CelebState, config: RunnableConfig):
    summary = state.get("summary", "")
    conversation_chain = get_celeb_response_chain()

    response = await conversation_chain.ainvoke(
        {
            "messages": state["messages"],
            "celeb_context": state["celeb_context"],
            "celeb_name": state["celeb_name"],
            "celeb_perspective": state["celeb_perspective"],
            "celeb_style": state["celeb_style"],
            "summary": summary,
        },
        config,
    )
    
    return {"messages": response}


async def summarize_conversation_node(state: CelebState):
    summary = state.get("summary", "")
    summary_chain = get_conversation_summary_chain(summary)

    response = await summary_chain.ainvoke(
        {
            "messages": state["messages"],
            "celeb_name": state["celeb_name"],
            "summary": summary,
        }
    )

    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]
    return {"summary": response.content, "messages": delete_messages}


async def summarize_context_node(state: CelebState):
    context_summary_chain = get_context_summary_chain()

    response = await context_summary_chain.ainvoke(
        {
            "context": state["messages"][-1].content,
        }
    )
    state["messages"][-1].content = response.content

    return {}


async def connector_node(state: CelebState):
    return {}