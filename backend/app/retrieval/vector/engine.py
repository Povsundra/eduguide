"""
Vector Retrieval Engine.
Executes semantic searches against the Qdrant database.
"""

import time
from typing import Dict, Any

from app.retrieval.interfaces.engine import BaseRetrievalEngine
from app.retrieval.models.request import RetrievalQuery
from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.vector.embedding import BaseEmbeddingProvider
from app.retrieval.vector.repository import BaseVectorSearchRepository
from app.retrieval.vector.normalizer import VectorScoreNormalizer


class VectorRetrievalEngine(BaseRetrievalEngine):
    """
    Retrieves semantically relevant knowledge from the vector database.
    """
    
    def __init__(
        self, 
        embedding_provider: BaseEmbeddingProvider,
        repository: BaseVectorSearchRepository, 
        normalizer: VectorScoreNormalizer = None,
        default_collection: str = "knowledge_chunks"
    ):
        self.embedding_provider = embedding_provider
        self.repository = repository
        self.normalizer = normalizer or VectorScoreNormalizer()
        self.default_collection = default_collection
        
    def can_handle(self, strategy: str) -> bool:
        return strategy in ["vector", "hybrid"]
        
    async def search(self, query: RetrievalQuery) -> RetrievalResponse:
        start_time = time.time()
        
        # 1. Generate Query Embedding
        vector = await self.embedding_provider.get_embedding(query.query_text)
        
        # 2. Determine Collection and Filters
        collection_name = query.filters.pop("collection", self.default_collection) if query.filters else self.default_collection
        
        # 3. Execute Vector Search
        raw_results = await self.repository.search(
            collection_name=collection_name,
            vector=vector,
            limit=query.top_k,
            filters=query.filters
        )
        
        # 4. Transform Results
        items = []
        for r in raw_results:
            raw_score = r.get("score", 0.0)
            item = RetrievalResultItem(
                item_id=r.get("id", ""),
                item_type="Document",
                content=r.get("payload", {}),
                score=0.0, # Will be set by normalizer
                metadata={"source": "Vector", "collection": collection_name, "raw_score": raw_score}
            )
            items.append(item)
            
        # 5. Normalize Scores
        normalized_items = self.normalizer.normalize(items)
        
        execution_time = (time.time() - start_time) * 1000
        
        return RetrievalResponse(
            query=query.query_text,
            results=normalized_items,
            execution_time_ms=execution_time
        )
