# Path: scaffold/core/blueprint_scribe/metadata_scribe.py
# -------------------------------------------------------
import getpass
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from ..alchemist import DivineAlchemist
from ... import __version__


class MetadataScribe:
    """
    =================================================================================
    == THE HISTORIAN (V-Ω-PROVENANCE-ENGINE)                                       ==
    =================================================================================
    [EVOLUTION 7] Dedicated handling of Gnostic Headers and Footers.
    """

    def __init__(self, project_root: Path, alchemist: DivineAlchemist):
        self.project_root = project_root
        self.alchemist = alchemist

    def forge_header(self, gnosis: Dict[str, Any]) -> List[str]:
        lines = []
        lines.append("# =================================================================================")
        lines.append(f"# == Gnostic Blueprint: {gnosis.get('project_name', self.project_root.name).title()}")
        lines.append(
            f"# == Forged by: {gnosis.get('author', getpass.getuser())} on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append("# =================================================================================")

        description_line = gnosis.get('description')
        if description_line:
            # Transmute description to resolve vars in comments
            rendered_desc = self.alchemist.transmute(description_line, gnosis)
            lines.append(f"# @description: {rendered_desc}")

        lines.append("#")
        for key in ['project_name', 'author', 'description']:
            if key in gnosis:
                val = str(gnosis[key]).replace('"', '\\"')
                lines.append(f"# @gnosis {key}: {val}")

        lines.append("# =================================================================================")
        lines.append("")
        return lines

    def forge_footer(self, gnosis: Dict[str, Any], commands: List[str]) -> List[str]:
        """
        [EVOLUTION 11] The Provenance Hasher.
        Calculates a hash of the variables to ensure integrity.
        """
        gnosis_for_hash = {k: v for k, v in gnosis.items() if
                           isinstance(v, (str, bool, int, float)) and not k.startswith('__')}

        # Include commands in hash for completeness
        gnosis_for_hash['__commands__'] = commands

        gnosis_hash_str = hashlib.sha256(json.dumps(gnosis_for_hash, sort_keys=True).encode('utf-8')).hexdigest()[:12]

        lines = []
        lines.append("")
        lines.append("# =================================================================================")
        lines.append("# == Gnostic Dossier of Provenance")
        lines.append("# =================================================================================")
        lines.append(f"# Scaffold Version:  {__version__}")
        lines.append(f"# Timestamp (UTC):   {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"# Gnosis Hash:       {gnosis_hash_str}")
        lines.append("# =================================================================================")
        return lines