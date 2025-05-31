from typing import Any
import json
from .base import ReportFormatter


class JSONFormatter(ReportFormatter):
    def format(self, report: Any) -> str:
        return json.dumps(report, indent=2, ensure_ascii=False)
