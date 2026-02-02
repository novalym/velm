# Path: artisans/analyze/redemption/healer.py
# -------------------------------------------

from pathlib import Path
from typing import List, Dict, Any


class RedemptionHealer:
    """
    =============================================================================
    == THE REDEMPTION HEALER (V-Ω-AUTO-CORRECT)                                ==
    =============================================================================
    """

    def __init__(self, engine):
        self.engine = engine

    def perform_auto_redemption(self, result, physical_path: Path, project_root: Path):
        """Attempts to fix reported heresies."""
        diagnostics = result.data.get("diagnostics", [])
        if not diagnostics: return

        redeemed = 0
        try:
            current_content = physical_path.read_text(encoding='utf-8')
        except:
            return

        # Lazy import to avoid cycle
        from ....interfaces.requests import RepairRequest

        for diag in diagnostics:
            code = str(diag.get('code', '')).upper()

            # Whitelist fixable codes
            if "UNDEFINED" in code or "REFERENCE_HERESY" in code:
                try:
                    req = RepairRequest(
                        file_path=str(physical_path),
                        content=current_content,
                        line_num=diag.get('data', {}).get('internal_line', 0) + 1,
                        heresy_key=code,
                        project_root=project_root,
                        context={"diagnostic": diag}
                    )

                    res = self.engine.dispatch(req)
                    if res.success and res.data and res.data.get('edits'):
                        self._apply_edits(physical_path, res.data['edits'])
                        redeemed += 1
                        # Reload content for next fix
                        current_content = physical_path.read_text(encoding='utf-8')
                except Exception:
                    pass

        if redeemed > 0:
            result.message += f" [Auto-Redeemed {redeemed} heresies]"
            result.data["redeemed_count"] = redeemed

    def _apply_edits(self, path: Path, edits: List[Dict]):
        try:
            content = path.read_text(encoding='utf-8')
            lines = content.splitlines(keepends=True)

            # Sort edits bottom-up
            sorted_edits = sorted(
                edits,
                key=lambda e: (e['range']['start']['line'], e['range']['start']['character']),
                reverse=True
            )

            for edit in sorted_edits:
                line_idx = int(edit['range']['start']['line'])
                if line_idx < len(lines):
                    # Simple replacement logic for now
                    lines[line_idx] = edit['newText'] + "\n"
                else:
                    lines.append(edit['newText'] + "\n")

            path.write_text("".join(lines), encoding='utf-8')
        except Exception:
            pass