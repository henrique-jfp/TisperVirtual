import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# Global client instance
_client = None


def _init_chroma_client():
    try:
        import chromadb
        from chromadb.config import Settings

        persist_dir = os.environ.get("CHROMA_PERSIST_DIR", ".chromadb")
        chroma_impl = os.environ.get("CHROMA_DB_IMPL", "duckdb+parquet")

        settings = Settings(chroma_db_impl=chroma_impl, persist_directory=persist_dir)
        client = chromadb.Client(settings=settings)
        logger.info(f"Chroma client initialized (persist={persist_dir})")
        return client
    except Exception as e:
        logger.debug(f"Chroma init failed: {e}")
        raise


def init_rag_client():
    """Initialize the RAG/vector client based on RAG_PROVIDER env var.

    Supported providers: chromadb
    """
    global _client
    if _client is not None:
        return _client

    provider = os.environ.get("RAG_PROVIDER", "chromadb").lower()

    if provider == "none" or provider == "":
        raise RuntimeError("RAG_PROVIDER is set to 'none' or empty — no vector DB will be used")

    if provider == "chromadb":
        try:
            _client = _init_chroma_client()
            return _client
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chroma client: {e}")

    raise RuntimeError(f"Unsupported RAG_PROVIDER '{provider}'. Supported: chromadb, none")


def get_collection(name: str = "futebol_data"):
    """Return a collection-like object with `query` and usual methods.

    This wraps the underlying provider's `get_or_create_collection`.
    """
    client = init_rag_client()
    # chromadb has get_or_create_collection
    try:
        return client.get_or_create_collection(name=name)
    except Exception as e:
        # rethrow with helpful message
        raise RuntimeError(f"Failed to get or create collection '{name}': {e}")
