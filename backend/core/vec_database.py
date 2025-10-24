from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, MatchValue, PointStruct
import os
from dotenv import load_dotenv
load_dotenv()

QDRANT_PASSWORD = os.getenv("QDRANT_PASSWORD", "")
QDRANT_HOST = os.getenv("QDRANT_HOST", "database-qdrant")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "ecp-ai")
QDRANT_SIZE = int(os.getenv("QDRANT_SIZE", 1024))
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"

client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_PASSWORD if QDRANT_PASSWORD != "" else None,
    )

if COLLECTION_NAME not in [col.name for col in client.get_collections().collections]:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=QDRANT_SIZE, distance=Distance.COSINE),
    )