"""
Duplicate Detector.
Detects duplicates in a batch of entities and relationships.
"""

from typing import List

from app.ingestion.models.entity import ExtractedEntity
from app.ingestion.models.relationship import ExtractedRelationship
from app.ingestion.models.duplicate import DuplicateReport, DuplicateResult, DuplicateType


class DuplicateDetector:
    """
    Detects intra-batch duplicates by checking exact entity and relationship IDs.
    In a real scenario, this would also query the Neo4j database to check against existing items.
    """

    def process(self, entities: List[ExtractedEntity], relationships: List[ExtractedRelationship]) -> DuplicateReport:
        report = DuplicateReport()
        
        seen_entity_ids = set()
        for e in entities:
            if e.entity_id in seen_entity_ids:
                report.results.append(
                    DuplicateResult(
                        duplicate_type=DuplicateType.ENTITY,
                        original_id=e.entity_id,
                        duplicate_id=e.entity_id,
                        reason="EXACT_ID_MATCH"
                    )
                )
                report.duplicates_found += 1
            else:
                seen_entity_ids.add(e.entity_id)
                report.unique_entities.append(e)

        seen_rel_ids = set()
        for r in relationships:
            if r.relationship_id in seen_rel_ids:
                report.results.append(
                    DuplicateResult(
                        duplicate_type=DuplicateType.RELATIONSHIP,
                        original_id=r.relationship_id,
                        duplicate_id=r.relationship_id,
                        reason="EXACT_ID_MATCH"
                    )
                )
                report.duplicates_found += 1
            else:
                seen_rel_ids.add(r.relationship_id)
                report.unique_relationships.append(r)
                
        return report
