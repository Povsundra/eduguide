"""
JSON Parser.
Basic implementation to convert arbitrary JSON payloads into structured elements.
"""

import json
from typing import Any, Dict

from app.ingestion.models.document import UnifiedDocument, DocumentType
from app.ingestion.models.structured import (
    StructuredDocument,
    StructuredSection,
    StructuredElement,
    ElementType
)
from app.ingestion.parsers.base import BaseParser


class JsonParser(BaseParser):
    """
    Parses JSON content into a StructuredDocument.
    Traverses the JSON tree and emits key-value pairs as headings and paragraphs/lists.
    """

    def parse(self, doc: UnifiedDocument) -> StructuredDocument:
        if doc.document_type != DocumentType.JSON:
            raise ValueError("JsonParser can only parse JSON documents.")

        try:
            data = json.loads(doc.content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON content: {str(e)}")

        root_section = StructuredSection(title="Root")
        
        # A simple recursive function to map JSON structures into sections
        def process_node(node_data: Any, parent_section: StructuredSection, key_name: str = None):
            if isinstance(node_data, dict):
                # Create a new subsection for this object if it has a key name
                target_section = parent_section
                if key_name:
                    new_sub = StructuredSection(title=key_name)
                    parent_section.subsections.append(new_sub)
                    target_section = new_sub
                
                for k, v in node_data.items():
                    process_node(v, target_section, k)
                    
            elif isinstance(node_data, list):
                # If it's a list of primitives, store as a LIST element
                if all(not isinstance(i, (dict, list)) for i in node_data):
                    parent_section.elements.append(
                        StructuredElement(
                            type=ElementType.LIST,
                            content=[str(i) for i in node_data],
                            properties={"key": key_name} if key_name else {}
                        )
                    )
                else:
                    # Complex list - create subsections for each item
                    target_section = parent_section
                    if key_name:
                        new_sub = StructuredSection(title=key_name)
                        parent_section.subsections.append(new_sub)
                        target_section = new_sub
                        
                    for i, item in enumerate(node_data):
                        process_node(item, target_section, f"Item {i+1}")
            else:
                # Primitive value
                content_str = str(node_data)
                # We can store the key as a property or prefix it in the text.
                # For this basic implementation, we just make it a paragraph.
                text = f"{key_name}: {content_str}" if key_name else content_str
                parent_section.elements.append(
                    StructuredElement(
                        type=ElementType.PARAGRAPH,
                        content=text
                    )
                )

        process_node(data, root_section)
        
        return StructuredDocument(
            document_id=doc.document_id,
            source_id=doc.source_id,
            metadata=doc.metadata,
            sections=[root_section]
        )
