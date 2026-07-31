"""
Hybrid Retrieval Orchestrator.
Coordinates multiple retrieval engines (Graph and Vector) and aggregates results.
"""

import asyncio
import time
import logging
from typing import List, Dict

from app.retrieval.interfaces.engine import BaseRetrievalEngine
from app.retrieval.models.request import RetrievalQuery
from app.retrieval.models.response import RetrievalResponse, RetrievalResultItem
from app.retrieval.ranking.engine import RankingEngine


logger = logging.getLogger(__name__)


class HybridRetrievalOrchestrator:
    """
    Coordinates Graph and Vector retrieval engines.
    """
    
    def __init__(self, engines: List[BaseRetrievalEngine], ranking_engine: RankingEngine = None, timeout_seconds: float = 5.0):
        self.engines = engines
        self.ranking_engine = ranking_engine or RankingEngine()
        self.timeout_seconds = timeout_seconds
        
    async def search(self, query: RetrievalQuery, strategy: str = "hybrid_parallel") -> RetrievalResponse:
        start_time = time.time()
        
        # 1. Select engines that can handle the strategy
        selected_engines = [e for e in self.engines if e.can_handle(strategy)]
        
        if not selected_engines:
            logger.warning(f"No retrieval engines found for strategy: {strategy}")
            return RetrievalResponse(query=query.query_text, results=[], execution_time_ms=0.0)
            
        # 2. Execute engines
        results = []
        if strategy == "hybrid_sequential":
            results = await self._execute_sequential(selected_engines, query)
        else:
            # graph, vector, hybrid_parallel all use parallel execution of the selected engines
            results = await self._execute_parallel(selected_engines, query)
            
        # 3. Aggregate results & detect duplicates using Ranking Engine
        aggregated = self.ranking_engine.rank(results, query.top_k)
        
        execution_time = (time.time() - start_time) * 1000
        
        return RetrievalResponse(
            query=query.query_text,
            results=aggregated,
            execution_time_ms=execution_time
        )
        
    async def _execute_parallel(
        self, 
        engines: List[BaseRetrievalEngine], 
        query: RetrievalQuery
    ) -> List[RetrievalResponse]:
        """
        Executes engines concurrently, enforcing timeout and handling failures gracefully.
        """
        tasks = []
        for engine in engines:
            task = asyncio.create_task(self._safe_execute_engine(engine, query))
            tasks.append(task)
            
        # Wait for all tasks to complete or timeout
        done, _ = await asyncio.wait(
            tasks, 
            timeout=self.timeout_seconds, 
            return_when=asyncio.ALL_COMPLETED
        )
        
        # Collect results, treating incomplete/failed as empty
        responses = []
        for task in tasks:
            if task.done() and not task.cancelled() and task.exception() is None:
                responses.append(task.result())
            else:
                logger.error(f"Engine execution failed or timed out: {task.exception() if task.done() else 'Timeout'}")
                
        return responses
        
    async def _execute_sequential(
        self, 
        engines: List[BaseRetrievalEngine], 
        query: RetrievalQuery
    ) -> List[RetrievalResponse]:
        """
        Executes sequentially. In a real system, the second engine might use results from the first.
        For this foundation, it just runs them one after another.
        """
        responses = []
        for engine in engines:
            try:
                # We enforce timeout per engine execution
                response = await asyncio.wait_for(engine.search(query), timeout=self.timeout_seconds)
                responses.append(response)
            except Exception as e:
                logger.error(f"Engine sequential execution failed: {e}")
                
        return responses
        
    async def _safe_execute_engine(self, engine: BaseRetrievalEngine, query: RetrievalQuery) -> RetrievalResponse:
        """Helper to catch exceptions within tasks."""
        try:
            return await engine.search(query)
        except Exception as e:
            logger.error(f"Engine search failed: {e}")
            raise
            

