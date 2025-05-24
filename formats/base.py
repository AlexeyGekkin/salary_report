from abc import ABC, abstractmethod
from typing import Any

class ReportFormatter(ABC):
    @abstractmethod
    def format(self, report: Any) -> str:
        pass