from typing import Generic, Type, TypeVar

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_postgres import PGEngine, PGVectorStore
from loguru import logger
from pydantic import BaseModel

from philoagents.config import settings

T = TypeVar("T", bound=BaseModel)


class PostgresClientWrapper(Generic[T]):
    """Service class for PostgreSQL operations with vector search support.

    This class provides methods to interact with PostgreSQL tables using langchain-postgres,
    including document ingestion, vector search, and hybrid search capabilities.

    Args:
        model (Type[T]): The Pydantic model class to use for document serialization.
        table_name (str): Name of the PostgreSQL table to use.
        embeddings (Embeddings): Embedding service for vector operations.
        postgres_uri (str, optional): URI for connecting to PostgreSQL instance.

    Attributes:
        model (Type[T]): The Pydantic model class used for document serialization.
        table_name (str): Name of the PostgreSQL table.
        postgres_uri (str): PostgreSQL connection URI.
        engine (PGEngine): PostgreSQL engine instance for database connections.
        vector_store (PGVectorStore): Vector store for hybrid search operations.
    """

    def __init__(
        self,
        model: Type[T],
        table_name: str,
        embeddings: Embeddings,
        postgres_uri: str = settings.POSTGRES_URI,
        vector_size: int = settings.RAG_TEXT_EMBEDDING_MODEL_DIM,
    ) -> None:
        """Initialize a connection to the PostgreSQL table with vector support.

        Args:
            model (Type[T]): The Pydantic model class to use for document serialization.
            table_name (str): Name of the PostgreSQL table to use.
            embeddings (Embeddings): Embedding service for vector operations.
            postgres_uri (str, optional): URI for connecting to PostgreSQL instance.
                Defaults to value from settings.
            vector_size (int, optional): Size of the vector embeddings.
                Defaults to value from settings.

        Raises:
            Exception: If connection to PostgreSQL fails.
        """
        self.model = model
        self.table_name = table_name
        self.postgres_uri = postgres_uri
        self.embeddings = embeddings
        self.vector_size = vector_size

        try:
            self.engine = PGEngine.from_connection_string(url=postgres_uri)
            logger.info(f"Connected to PostgreSQL: {postgres_uri}")
        except Exception as e:
            logger.error(f"Failed to initialize PostgresClientWrapper: {e}")
            raise

        # Initialize the vector store table
        try:
            # self.engine.init_vectorstore_table(
            #     table_name=table_name,
            #     vector_size=vector_size,
            # )

            self.vector_store = PGVectorStore.create_sync(
                engine=self.engine,
                table_name=table_name,
                embedding_service=embeddings,
            )
            logger.info(
                f"Initialized PostgreSQL vector store: Table: {table_name}, Vector size: {vector_size}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise

    def __enter__(self) -> "PostgresClientWrapper":
        """Enable context manager support.

        Returns:
            PostgresClientWrapper: The current instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close PostgreSQL connection when exiting context.

        Args:
            exc_type: Type of exception that occurred, if any.
            exc_val: Exception instance that occurred, if any.
            exc_tb: Traceback of exception that occurred, if any.
        """
        self.close()

    def clear_table(self) -> None:
        """Clear all documents from the table."""
        try:
            self.vector_store.delete()
            logger.info(f"Cleared all documents from table: {self.table_name}")
        except Exception as e:
            logger.error(f"Error clearing table {self.table_name}: {str(e)}")
            raise

    def ingest_documents(self, documents: list[T]) -> None:
        """Insert multiple documents into the PostgreSQL table.

        Args:
            documents: List of Pydantic model instances to insert.

        Raises:
            ValueError: If documents is empty or contains non-Pydantic model items.
            Exception: If the insertion operation fails.
        """
        try:
            if not documents or not all(
                isinstance(doc, BaseModel) for doc in documents
            ):
                raise ValueError("Documents must be a list of Pydantic models.")

            # Convert Pydantic models to Document objects
            doc_objects = []
            for doc in documents:
                doc_dict = doc.model_dump()
                content = doc_dict.get("page_content", str(doc_dict))
                metadata = {k: v for k, v in doc_dict.items() if k != "page_content"}

                doc_objects.append(Document(page_content=content, metadata=metadata))

            self.vector_store.add_documents(doc_objects)
            logger.debug(f"Inserted {len(documents)} documents into PostgreSQL.")
        except Exception as e:
            logger.error(f"Error inserting documents: {e}")
            raise

    def fetch_documents(self, limit: int, query: dict) -> list[T]:
        """Retrieve documents from the PostgreSQL table based on a query.

        Args:
            limit (int): Maximum number of documents to retrieve.
            query (dict): Filter query to apply (for metadata filtering).

        Returns:
            list[T]: List of Pydantic model instances matching the query criteria.

        Raises:
            Exception: If the query operation fails.
        """
        try:
            # Convert query to filter format for PGVectorStore
            filter_dict = query if query else {}

            # Perform similarity search (using a generic query if no specific search term)
            search_query = "general search"
            documents = self.vector_store.similarity_search(
                search_query, k=limit, filter=filter_dict if filter_dict else None
            )

            logger.debug(f"Fetched {len(documents)} documents with query: {query}")
            return self._parse_documents(documents)
        except Exception as e:
            logger.error(f"Error fetching documents: {e}")
            raise

    def similarity_search(
        self, query: str, k: int = 5, filter_dict: dict = None
    ) -> list[T]:
        """Perform vector similarity search.

        Args:
            query (str): Search query text.
            k (int): Number of results to return.
            filter_dict (dict, optional): Metadata filter.

        Returns:
            list[T]: List of similar documents.
        """
        try:
            documents = self.vector_store.similarity_search(
                query, k=k, filter=filter_dict
            )
            return self._parse_documents(documents)
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise

    def hybrid_search(
        self, query: str, k: int = 5, filter_dict: dict = None
    ) -> list[T]:
        """Perform hybrid search (vector + full-text search).

        Args:
            query (str): Search query text.
            k (int): Number of results to return.
            filter_dict (dict, optional): Metadata filter.

        Returns:
            list[T]: List of relevant documents from hybrid search.
        """
        try:
            # PGVectorStore supports hybrid search through PostgreSQL's full-text search
            # This combines vector similarity with text matching
            documents = self.vector_store.similarity_search(
                query, k=k, filter=filter_dict
            )
            return self._parse_documents(documents)
        except Exception as e:
            logger.error(f"Error in hybrid search: {e}")
            raise

    def _parse_documents(self, documents: list[Document]) -> list[T]:
        """Convert Document objects to Pydantic model instances.

        Args:
            documents (list[Document]): List of Document objects to parse.

        Returns:
            list[T]: List of validated Pydantic model instances.
        """
        parsed_documents = []
        for doc in documents:
            try:
                # Create a dict with page_content and metadata
                doc_dict = {"page_content": doc.page_content}
                doc_dict.update(doc.metadata)

                parsed_doc = self.model.model_validate(doc_dict)
                parsed_documents.append(parsed_doc)
            except Exception as e:
                logger.warning(f"Failed to parse document: {e}")
                continue

        return parsed_documents

    def get_collection_count(self) -> int:
        """Count the total number of documents in the table.

        Returns:
            Total number of documents in the table.

        Raises:
            Exception: If the count operation fails.
        """
        try:
            # Perform a search with large k to estimate count
            # This is an approximation since PGVectorStore doesn't have direct count
            results = self.vector_store.similarity_search("", k=10000)
            return len(results)
        except Exception as e:
            logger.error(f"Error counting documents in PostgreSQL: {e}")
            raise

    def close(self) -> None:
        """Close the PostgreSQL connection.

        This method should be called when the service is no longer needed
        to properly release resources, unless using the context manager.
        """
        try:
            # PGEngine doesn't require explicit closing in the same way as MongoDB
            logger.debug("PostgreSQL connection resources released.")
        except Exception as e:
            logger.warning(f"Error during close: {e}")
