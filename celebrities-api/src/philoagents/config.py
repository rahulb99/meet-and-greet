from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    # --- GROQ Configuration ---
    GROQ_API_KEY: str
    GROQ_LLM_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_LLM_MODEL_CONTEXT_SUMMARY: str = "llama-3.1-8b-instant"
    GROQ_LLM_MODEL_SUMMARY: str = "llama-3.1-8b-instant"

    # --- OpenAI Configuration (Required for evaluation) ---
    OPENAI_API_KEY: str

    # --- PostgreSQL Configuration ---
    POSTGRES_URI: str = Field(
        default="postgres://celebrities:celebrities@postgres:5432/celebrities?sslmode=disable",
        description="Connection URI for the PostgreSQL instance.",
    )
    POSTGRES_DB_NAME: str = "celebrities"
    POSTGRES_STATE_CHECKPOINT_TABLE: str = "celeb_state_checkpoints"
    POSTGRES_STATE_WRITES_TABLE: str = "celeb_state_writes"
    POSTGRES_LONG_TERM_MEMORY_TABLE: str = "celeb_long_term_memory"

    # --- Comet ML & Opik Configuration ---
    COMET_API_KEY: str | None = Field(
        default=None, description="API key for Comet ML and Opik services."
    )
    COMET_PROJECT: str = Field(
        default="meet-and-greet",
        description="Project name for Comet ML and Opik tracking.",
    )

    # --- Agents Configuration ---
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 30
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5

    # --- RAG Configuration ---
    RAG_TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_TEXT_EMBEDDING_MODEL_DIM: int = 384
    RAG_TOP_K: int = 5
    RAG_DEVICE: str = "cpu"
    RAG_CHUNK_SIZE: int = 256

    # --- Paths Configuration ---
    EVALUATION_DATASET_FILE_PATH: Path = Path("data/evaluation_dataset.json")
    EXTRACTION_METADATA_FILE_PATH: Path = Path("data/extraction_metadata.json")


settings = Settings()
