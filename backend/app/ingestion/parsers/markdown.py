"""
Markdown Parser.
Basic implementation to split Markdown into sections and elements.
"""

import re
from typing import List

from app.ingestion.models.document import UnifiedDocument, DocumentType
from app.ingestion.models.structured import (
    StructuredDocument,
    StructuredSection,
    StructuredElement,
    ElementType
)
from app.ingestion.parsers.base import BaseParser


class MarkdownParser(BaseParser):
    """
    Parses Markdown content into a StructuredDocument.
    Implements a basic line-by-line state machine for extracting headings, paragraphs, and lists.
    """

    def parse(self, doc: UnifiedDocument) -> StructuredDocument:
        if doc.document_type != DocumentType.MARKDOWN:
            raise ValueError("MarkdownParser can only parse MARKDOWN documents.")

        lines = doc.content.split('\n')
        
        # Root sections (everything before the first heading goes into a default root section, or we wrap it)
        root_sections: List[StructuredSection] = []
        
        current_section = StructuredSection(title="Root")
        root_sections.append(current_section)
        
        # Stack to keep track of heading hierarchy
        section_stack = [(0, current_section)]
        
        current_paragraph_lines = []
        current_list_items = []

        def flush_paragraph():
            if current_paragraph_lines:
                text = " ".join(current_paragraph_lines).strip()
                if text:
                    section_stack[-1][1].elements.append(
                        StructuredElement(type=ElementType.PARAGRAPH, content=text)
                    )
                current_paragraph_lines.clear()

        def flush_list():
            if current_list_items:
                section_stack[-1][1].elements.append(
                    StructuredElement(type=ElementType.LIST, content=list(current_list_items))
                )
                current_list_items.clear()

        for line in lines:
            stripped = line.strip()
            
            # Heading matching
            heading_match = re.match(r'^(#{1,6})\s+(.*)', stripped)
            if heading_match:
                flush_paragraph()
                flush_list()
                
                level = len(heading_match.group(1))
                title = heading_match.group(2)
                
                new_section = StructuredSection(title=title)
                
                # Pop the stack until we find a parent with a lower level
                while len(section_stack) > 1 and section_stack[-1][0] >= level:
                    section_stack.pop()
                    
                # Add as subsection to the current parent
                section_stack[-1][1].subsections.append(new_section)
                
                # Push new section to stack
                section_stack.append((level, new_section))
                continue

            # List item matching
            list_match = re.match(r'^[-*+]\s+(.*)', stripped)
            if list_match:
                flush_paragraph()
                current_list_items.append(list_match.group(1))
                continue
                
            # Empty line
            if not stripped:
                flush_paragraph()
                flush_list()
                continue
                
            # Regular text (paragraph continuation)
            flush_list()
            current_paragraph_lines.append(stripped)

        # Flush any remaining items at EOF
        flush_paragraph()
        flush_list()

        # If the root section is empty and only has subsections, we can flatten it,
        # but returning it as-is is safer and structurally consistent.
        
        return StructuredDocument(
            document_id=doc.document_id,
            source_id=doc.source_id,
            metadata=doc.metadata,
            sections=root_sections
        )
