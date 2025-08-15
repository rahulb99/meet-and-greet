from langchain_postgres.v2.indexes import HNSWIndex, IVFFlatIndex

from .client import PostgresClientWrapper


class PostgresIndex:
    """PostgreSQL index management for vector search optimization."""

    def __init__(
        self,
        retriever,
        postgres_client: PostgresClientWrapper,
    ) -> None:
        self.retriever = retriever
        self.postgres_client = postgres_client

    def create(
        self,
        embedding_dim: int,
        is_hybrid: bool = False,
        index_type: str = "hnsw",
    ) -> None:
        """Create vector search indexes.

        Args:
            embedding_dim (int): Dimension of the embedding vectors.
            is_hybrid (bool): Whether to enable hybrid search capabilities.
            index_type (str): Type of index to create ("hnsw" or "ivfflat").
        """
        vector_store = self.postgres_client.vector_store

        if index_type.lower() == "hnsw":
            index = HNSWIndex(name=f"{self.postgres_client.table_name}_hnsw_index")
        else:
            index = IVFFlatIndex(
                name=f"{self.postgres_client.table_name}_ivfflat_index"
            )

        # Apply the vector index
        vector_store.apply_vector_index(index)

        if is_hybrid:
            # PostgreSQL full-text search is automatically available with PGVectorStore
            # No additional setup needed for hybrid search as it's built into PostgreSQL
            pass
