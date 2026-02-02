# Path: repair/surgery.py
# -----------------------
from pathlib import Path
from typing import List, Any, Dict

class SurgicalRouter:
    """
    The Operating Theatre.
    Determines if a heresy requires AST surgery and performs it.
    """

    # Heresies that require full AST parsing/rewriting
    SURGICAL_KEYS = {"BROKEN_IMPORT", "MODULE_NOT_FOUND", "IMPORT_ERROR", "UNRESOLVED_IMPORT"}

    @classmethod
    def can_handle(cls, heresy_key: str) -> bool:
        return any(k in heresy_key.upper() for k in cls.SURGICAL_KEYS)

    @classmethod
    def operate(cls, request: Any, project_root: Path) -> List[Dict[str, Any]]:
        """
        Performs AST surgery and returns a FULL FILE REPLACEMENT edit.
        Returns raw LSP-compliant dictionaries.
        """
        # Divine Summons inside the method to prevent circular imports
        from ...inquisitor.python_inquisitor import PythonCodeInquisitor
        from ...artisans.translocate_core.resolvers import PythonImportResolver
        from ...artisans.heal.healers.python_import_healer import PythonImportHealer

        # 1. Forge the Context (Symbol Map)
        inquisitor = PythonCodeInquisitor(project_root).inquire_project()
        if not inquisitor.symbol_map:
            return []

        # 2. Summon the Healer
        resolver = PythonImportResolver(project_root, inquisitor.symbol_map, {})
        context = {'python_resolver': resolver}
        healer = PythonImportHealer(project_root, context)

        # 3. Diagnose & Heal
        file_path = Path(request.file_path)
        diagnoses = healer.diagnose(file_path, request.content)

        if not diagnoses:
            return []

        new_content, changed = healer.heal(file_path, request.content, diagnoses)

        if changed:
            # AST Surgery replaces the entire file content.
            # We return a single edit covering the whole document.
            line_count = len(request.content.splitlines())
            return [{
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": line_count + 1, "character": 0}
                },
                "newText": new_content
            }]

        return []