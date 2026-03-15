# Path: parser_core/lexer_core/inquisitor/forensics.py
# ----------------------------------------------------

import traceback
from pathlib import Path
from typing import Union, TYPE_CHECKING

from ....contracts.data_contracts import GnosticVessel, ScaffoldItem
from ....contracts.heresy_contracts import HeresySeverity

if TYPE_CHECKING:
    from ...parser.engine import ApotheosisParser


class TriageForensics:
    """
    =============================================================================
    == THE TRIAGE FORENSICS ORGAN (V-Ω-TOTALITY)                               ==
    =============================================================================
    LIF: ∞ | ROLE: PARADOX_RADIATOR
    Handles all exception un-wrapping and HUD radiation for the Inquisitor.
    """

    @classmethod
    def proclaim_heresy(
            cls,
            parser: 'ApotheosisParser',
            key: str,
            item: Union[GnosticVessel, ScaffoldItem, str],
            **kwargs
    ):
        """Delegates the forging of the heresy vessel to the universal rite."""
        from ....jurisprudence_core.jurisprudence import forge_heresy_vessel

        raw_scripture = getattr(item, 'raw_scripture', str(item))
        line_num = getattr(item, 'line_num', 0)
        exception_obj = kwargs.get('exception_obj')
        details = kwargs.get('details', "")

        # [ASCENSION 32003]: Socratic Error Unwrapping
        if exception_obj:
            tb_list = traceback.extract_tb(exception_obj.__traceback__)
            scaffold_frames = [f for f in tb_list if 'scaffold' in f.filename or 'velm' in f.filename]
            last_frame = scaffold_frames[-1] if scaffold_frames else tb_list[-1]
            report = f"Paradox: {type(exception_obj).__name__} | Locus: {Path(last_frame.filename).name}:{last_frame.lineno}"
            details = f"{details}\n{report}"

        heresy = forge_heresy_vessel(key=key, line_num=line_num, line_content=raw_scripture, details=details)

        if severity_override := kwargs.get('severity'):
            heresy.severity = severity_override

        parser.heresies.append(heresy)

        if hasattr(item, 'is_valid'):
            item.is_valid = False

        if heresy.severity == HeresySeverity.CRITICAL:
            parser.all_rites_are_pure = False