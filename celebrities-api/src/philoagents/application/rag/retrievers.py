from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.vectorstores import VectorStoreRetriever
    from langchain_huggingface import HuggingFaceEmbeddings

from philoagents.config import settings

from .embeddings import get_embedding_model

# Type alias for the retriever - using basic VectorStore retriever for now
Retriever = "VectorStoreRetriever"


def get_retriever(
    embedding_model_id: str,
    k: int = 3,
    device: str = "cpu",
) -> "VectorStoreRetriever":
    """Creates and returns a retriever with the specified embedding model.

    Args:
        embedding_model_id (str): The identifier for the embedding model to use.
        k (int, optional): Number of documents to retrieve. Defaults to 3.
        device (str, optional): Device to run the embedding model on. Defaults to "cpu".

    Returns:
        VectorStoreRetriever: A configured search retriever.
    """
    from loguru import logger

    logger.info(
        f"Initializing retriever | model: {embedding_model_id} | device: {device} | top_k: {k}"
    )

    embedding_model = get_embedding_model(embedding_model_id, device)

    return get_hybrid_search_retriever(embedding_model, k)


def get_hybrid_search_retriever(
    embedding_model: "HuggingFaceEmbeddings", k: int
) -> "VectorStoreRetriever":
    """Creates a PostgreSQL retriever with the given embedding model.

    Args:
        embedding_model (HuggingFaceEmbeddings): The embedding model to use for vector search.
        k (int): Number of documents to retrieve.

    Returns:
        VectorStoreRetriever: A configured search retriever.
    """
    from langchain_postgres import PGEngine, PGVectorStore

    # Create the PG engine
    engine = PGEngine.from_connection_string(url=settings.POSTGRES_URI)

    # # Initialize the vector store table with proper schema
    engine.init_vectorstore_table(
        table_name=settings.POSTGRES_LONG_TERM_MEMORY_TABLE,
        overwrite_existing=True,
        vector_size=settings.RAG_TEXT_EMBEDDING_MODEL_DIM,
    )

    # Create the vector store
    vectorstore = PGVectorStore.create_sync(
        engine=engine,
        table_name=settings.POSTGRES_LONG_TERM_MEMORY_TABLE,
        embedding_service=embedding_model,
        distance_strategy="cosine",
    )

    # Return the vector store as a retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    return retriever
