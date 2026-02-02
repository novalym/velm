# Path: scaffold/artisans/canon/law.py
# ------------------------------------
from dataclasses import dataclass
from typing import List, Pattern
import re

@dataclass
class CanonLaw:
    name: str
    source_pattern: str # Regex for source file path
    forbidden_imports: List[str] # List of forbidden module prefixes
    severity: str = "CRITICAL"

class LawEngine:
    def adjudicate(self, file_path: str, imports: List[str], laws: List[CanonLaw]) -> List[str]:
        violations = []
        for law in laws:
            if re.search(law.source_pattern, file_path):
                for imp in imports:
                    for forbidden in law.forbidden_imports:
                        if imp.startswith(forbidden):
                            violations.append(f"Heresy: '{file_path}' imports '{imp}', violating '{law.name}' (Forbidden: {forbidden})")
        return violations