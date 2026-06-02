"""Port for CV parsers. Implementations live in app/services/cv_parsing."""
from abc import ABC, abstractmethod

from app.schemas.cv_schema import CVSections


class CVParser(ABC):
    @abstractmethod
    def parse(self, raw_text: str) -> CVSections:
        """Turn raw CV text into a normalized section structure."""
        raise NotImplementedError
