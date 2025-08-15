import asyncpg
from loguru import logger

from philoagents.config import settings


async def reset_conversation_state() -> dict:
    """Deletes all conversation state data from PostgreSQL.

    This function removes all stored conversation checkpoints and writes,
    effectively resetting all celeb conversations.

    Returns:
        dict: Status message indicating success or failure with details
              about which tables were cleared

    Raises:
        Exception: If there's an error connecting to PostgreSQL or clearing tables
    """
    try:
        # Parse the PostgreSQL URI to extract connection parameters
        import urllib.parse as urlparse

        parsed = urlparse.urlparse(settings.POSTGRES_URI)

        conn = await asyncpg.connect(
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:],  # Remove leading '/'
            host=parsed.hostname,
            port=parsed.port or 5432,
        )

        tables_cleared = []

        # Clear checkpoints table
        try:
            await conn.execute(
                f"DELETE FROM {settings.POSTGRES_STATE_CHECKPOINT_TABLE}"
            )
            tables_cleared.append(settings.POSTGRES_STATE_CHECKPOINT_TABLE)
            logger.info(f"Cleared table: {settings.POSTGRES_STATE_CHECKPOINT_TABLE}")
        except Exception:
            logger.warning(
                f"Table {settings.POSTGRES_STATE_CHECKPOINT_TABLE} does not exist or couldn't be cleared"
            )

        # Clear writes table
        try:
            await conn.execute(f"DELETE FROM {settings.POSTGRES_STATE_WRITES_TABLE}")
            tables_cleared.append(settings.POSTGRES_STATE_WRITES_TABLE)
            logger.info(f"Cleared table: {settings.POSTGRES_STATE_WRITES_TABLE}")
        except Exception:
            logger.warning(
                f"Table {settings.POSTGRES_STATE_WRITES_TABLE} does not exist or couldn't be cleared"
            )

        await conn.close()

        if tables_cleared:
            return {
                "status": "success",
                "message": f"Successfully cleared tables: {', '.join(tables_cleared)}",
            }
        else:
            return {
                "status": "success",
                "message": "No tables needed to be cleared",
            }

    except Exception as e:
        logger.error(f"Failed to reset conversation state: {str(e)}")
        raise Exception(f"Failed to reset conversation state: {str(e)}")
