"""
Pipeline Logger.
Centralized logging and metrics tracking for the ingestion pipeline.
"""

import logging
import time
from typing import Dict, Any


class PipelineLogger:
    """
    Tracks events and metrics for the ingestion pipeline.
    """
    
    def __init__(self, name: str = "IngestionPipeline"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        # In a real app we would add handlers, but for testing we just track internal state
        
        self.metrics: Dict[str, Any] = {
            "documents_processed": 0,
            "documents_failed": 0,
            "entities_created": 0,
            "relationships_created": 0,
            "duplicates_found": 0,
            "validation_errors": 0,
            "execution_time_sec": 0.0,
            "start_time": 0.0
        }
        
    def start_pipeline(self):
        self.metrics["start_time"] = time.time()
        self.logger.info("Pipeline started")
        
    def end_pipeline(self):
        end_time = time.time()
        self.metrics["execution_time_sec"] = end_time - self.metrics["start_time"]
        self.logger.info("Pipeline finished")
        
    def record_document_success(self):
        self.metrics["documents_processed"] += 1
        
    def record_document_failure(self):
        self.metrics["documents_failed"] += 1
        
    def record_entities(self, count: int):
        self.metrics["entities_created"] += count
        
    def record_relationships(self, count: int):
        self.metrics["relationships_created"] += count
        
    def record_duplicates(self, count: int):
        self.metrics["duplicates_found"] += count
        
    def log_error(self, stage: str, document_id: str, error: Exception):
        self.metrics["validation_errors"] += 1
        self.logger.error(f"Error in {stage} for doc {document_id}: {str(error)}")
