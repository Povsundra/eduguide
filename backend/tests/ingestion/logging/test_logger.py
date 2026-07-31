"""
Tests for Subphase 4.12 - Logging & Error Handling
"""

from app.ingestion.logging.logger import PipelineLogger


def test_pipeline_logger():
    logger = PipelineLogger()
    
    logger.start_pipeline()
    logger.record_document_success()
    logger.record_document_failure()
    logger.record_entities(5)
    logger.record_relationships(2)
    logger.record_duplicates(1)
    logger.log_error("Validation", "doc_1", Exception("Test Error"))
    logger.end_pipeline()
    
    assert logger.metrics["documents_processed"] == 1
    assert logger.metrics["documents_failed"] == 1
    assert logger.metrics["entities_created"] == 5
    assert logger.metrics["relationships_created"] == 2
    assert logger.metrics["duplicates_found"] == 1
    assert logger.metrics["validation_errors"] == 1
    assert logger.metrics["execution_time_sec"] >= 0
