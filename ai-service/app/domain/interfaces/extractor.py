"""Port for document text extractors (PDF, DOCX, ...).

An extractor turns raw file bytes into plain text. Section extraction is a
separate concern handled by the CVNormalizer (see parser.py).
"""
from abc import ABC, abstractmethod


class TextExtractor(ABC):
    #: File extensions this extractor handles, lowercase, with leading dot.
    suffixes: tuple[str, ...] = ()
    #: MIME types this extractor handles.
    content_types: tuple[str, ...] = ()

    @abstractmethod
    def extract(self, content: bytes) -> str:
        """Extract plain text from the given file bytes."""
        raise NotImplementedError
