"""
Graph Retrieval Engine.
Executes graph searches against Neo4j using the repository.
"""

import time
from typing import List, Dict, Any

from app.retrieval.interfaces.engine import BaseRetrievalEngine
from app.retrieval.models.request import RetrievalQuery
from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.graph.repository import BaseGraphSearchRepository
from app.retrieval.graph.normalizer import GraphScoreNormalizer


class GraphRetrievalEngine(BaseRetrievalEngine):
    """
    Retrieves structured knowledge from the graph database.
    """
    
    def __init__(self, repository: BaseGraphSearchRepository, normalizer: GraphScoreNormalizer = None):
        self.repository = repository
        self.normalizer = normalizer or GraphScoreNormalizer()
        
    def can_handle(self, strategy: str) -> bool:
        return strategy in ["graph", "hybrid"]
        
    async def search(self, query: RetrievalQuery) -> RetrievalResponse:
        start_time = time.time()
        
        # 1. Build the Cypher query and parameters
        cypher, parameters = self._build_cypher_query(query)
        
        # 2. Execute query via repository
        raw_results = await self.repository.execute_query(cypher, parameters)
        
        # 3. Process raw results into standardized result items
        items = self._process_results(raw_results)
        
        # 4. Normalize scores and sort
        normalized_items = self.normalizer.normalize(items)
        
        # 5. Apply top_k
        final_items = normalized_items[:query.top_k]
        
        execution_time = (time.time() - start_time) * 1000
        
        return RetrievalResponse(
            query=query.query_text,
            results=final_items,
            execution_time_ms=execution_time
        )
        
    def _build_cypher_query(self, query: RetrievalQuery) -> tuple[str, Dict[str, Any]]:
        """
        Dynamically constructs parameterized Cypher based on query text and filters.
        """
        # For this foundation phase, we're building a generic neighborhood search query.
        # This searches for entities matching the text, optionally filtered by entity_type,
        # and expands to their immediate neighbors (hops=1).
        
        base_match = "MATCH (n) WHERE toLower(n.name) CONTAINS toLower($query_text)"
        
        parameters = {"query_text": query.query_text}
        
        # Add metadata filtering (e.g. entity_type)
        if query.filters:
            if "entity_type" in query.filters:
                base_match += " AND n.entity_type = $entity_type"
                parameters["entity_type"] = query.filters["entity_type"]
                
        # We also want neighbors
        cypher = f"""
        {base_match}
        OPTIONAL MATCH (n)-[r]-(neighbor)
        RETURN n.id AS root_id, n.entity_type AS root_type, n.name AS root_name,
               type(r) AS rel_type,
               neighbor.id AS neighbor_id, neighbor.entity_type AS neighbor_type, neighbor.name AS neighbor_name
        LIMIT $limit
        """
        
        parameters["limit"] = query.top_k * 5 # Get more raw results to filter down
        
        return cypher, parameters
        
    def _process_results(self, raw_results: List[Dict[str, Any]]) -> List[RetrievalResultItem]:
        """
        Converts Cypher result rows into normalized result items.
        """
        items_map = {}
        
        for row in raw_results:
            root_id = row.get("root_id")
            if not root_id:
                continue
                
            # Add root item (hops=0)
            if root_id not in items_map:
                items_map[root_id] = RetrievalResultItem(
                    item_id=root_id,
                    item_type=row.get("root_type", "Entity"),
                    content={"name": row.get("root_name")},
                    score=1.0,
                    metadata={"hops": 0, "source": "Graph"}
                )
                
            # Add neighbor item (hops=1)
            neighbor_id = row.get("neighbor_id")
            if neighbor_id and neighbor_id not in items_map:
                items_map[neighbor_id] = RetrievalResultItem(
                    item_id=neighbor_id,
                    item_type=row.get("neighbor_type", "Entity"),
                    content={"name": row.get("neighbor_name")},
                    score=1.0, # Will be normalized
                    metadata={"hops": 1, "source": "Graph", "related_via": row.get("rel_type")}
                )
                
        return list(items_map.values())
