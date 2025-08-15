from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools import DuckDuckGoSearchRun

from philoagents.application.rag.retrievers import get_retriever
from philoagents.config import settings

retriever = get_retriever(
    embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
    k=settings.RAG_TOP_K,
    device=settings.RAG_DEVICE)

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_celeb_context",
    "Search and return information about a specific celeb. Always use this tool when the user asks you about a celeb, their work, accomplishments or journey.",
)

duckduckgo_search_tool = DuckDuckGoSearchRun(description="Always use this tool when the user asks about latest/current information about a celeb or their work.")

tools = [retriever_tool, duckduckgo_search_tool]