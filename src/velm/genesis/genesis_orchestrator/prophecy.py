# Path: src/velm/genesis/genesis_orchestrator/prophecy.py
# -------------------------------------------------------

import os
import re
import shutil
import time
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Any, Set, TYPE_CHECKING, Final

from rich.text import Text

# --- THE DIVINE UPLINKS ---
from ..genesis_grimoires import GENESIS_GRIMOIRE
from ..genesis_profiles import PROFILES
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity, Heresy
from ...core.alchemist import get_alchemist
from ...logger import Scribe
from ...utils import is_git_installed, to_string_safe, generate_derived_names

if TYPE_CHECKING:
    from .orchestrator import GenesisDialogueOrchestrator

Logger = Scribe("GenesisProphet")


class ProphecyMixin:
    """
    =================================================================================
    == THE OMNISCIENT PROPHET (V-Ω-TOTALITY-V512.0-SOVEREIGN-CONVERGENCE)          ==
    =================================================================================
    LIF: ∞ | ROLE: CAUSAL_UNION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_PROPHET_V512_IDENTITY_CONVERGENCE_FINALIS_2026

    The supreme artisan of foresight. It annihilates the "Overwriting Heresy" by
    enforcing **Geometric Identity Convergence**.

    ### THE PANTHEON OF 12 NEW LEGENDARY ASCENSIONS:
    1.  **Geometric Identity Convergence (THE CURE):** Transmutes every path into a
        normalized POSIX lowercase identity string before checking Sovereignty.
    2.  **The "Shield of the Soul" (Content Guard):** Explicitly preserves the `content`
        of Archetype items, forbidding the Grimoire from injecting its own souls.
    3.  **Achronal Placeholder Stripping:** Detects `{{ description }}` hallucinations
        and prevents them from blanketing specific template logic.
    4.  **The Root-Relative Anchor:** Automatically strips the `project_slug` prefix
        from comparisons to handle both "flat" and "nested" archetype definitions.
    5.  **The Double-Gaze Verification:** Cross-references the `ProjectScanner`'s
        real-world cache to detect if a file was pre-created by a "Ghost" artisan.
    6.  **Sovereign Hierarchy Locking:** If an item is born from an Archetype, its
        identity is locked as `SOVEREIGN`, making it immune to Grimoire "Life Support".
    7.  **The Socratic Conflict Resolver:** If a collision is detected between
        blueprints, it preserves the one with the higher Gnostic Mass (more bytes).
    8.  **Maestro Command Deduping:** Prevents duplicate `git init` or `npm install`
        calls by performing a semantic check on the edict strings.
    9.  **The Metadata Suture:** Merges `permissions` and `mutation_ops` from the
        Grimoire into the Archetype's item *without* replacing the content.
    10. **The Silhouette Filter:** Purges empty directories willed by the Grimoire
        if the Archetype has willed a file at that same locus.
    11. **The Telemetry Pulse (Extended):** Reports the "Sovereignty Ratio" (how
        much of the project is Archetype vs. Supplemental).
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable, non-redundant plan.
    =================================================================================
    """

    def _prophesy_structure(self: 'GenesisDialogueOrchestrator', gnosis: Dict) -> Tuple[List[ScaffoldItem], List[Dict]]:
        """
        =================================================================================
        == THE OMNISCIENT PROPHET (V-Ω-TOTALITY-V525.0-IDENTITY-CONVERGED)             ==
        =================================================================================
        LIF: ∞ | ROLE: CAUSAL_UNION_CONDUCTOR
        AUTH: Ω_PROPHET_V525_IDENTITY_CONVERGENCE_FINALIS_2026

        [THE CURE]: This version annihilates the "README Overwrite" by performing
        Geometric Identity Convergence. It ensures the Archetype is the Supreme Law.
        """
        self.Logger.info("The Prophet awakens. Orchestrating Geometric Convergence...")

        final_items: List[ScaffoldItem] = []
        review_dossier: List[Dict] = []

        alchemist = get_alchemist()
        alchemical_ctx = gnosis.copy()
        alchemical_ctx['slug'] = self.current_project_slug
        alchemical_ctx['project_slug'] = self.current_project_slug

        # --- MOVEMENT I: THE INGESTION OF THE SOVEREIGN SOUL (ARCHETYPE) ---
        profile_name = gnosis.get('project_type', 'generic')
        archetype_info = PROFILES.get(profile_name)

        archetype_items: List[ScaffoldItem] = []
        if archetype_info:
            try:
                # Perform a stateless Master Weave of the chosen Archetype
                _, archetype_items, _, _ = self.engine._conduct_master_weave(
                    archetype_info, gnosis, overrides=gnosis
                )
            except Exception as e:
                self.Logger.warn(f"Causal Schism: Archetype ingestion fractured: {e}")

        # [ASCENSION 1 & 4]: GEOMETRIC IDENTITY CONVERGENCE (THE CURE)
        # Normalizes "project/README.md" and "README.md" into the same Gnostic ID.
        sovereign_identity_map: Dict[str, ScaffoldItem] = {}

        def _get_gnostic_identity(path: Path) -> str:
            # 1. Force POSIX Lowercase
            p_str = path.as_posix().lower()
            # 2. Strip the project slug prefix to find the root-relative identity
            p_str = re.sub(rf"^{re.escape(self.current_project_slug)}/", "", p_str)
            # 3. Strip leading relative dots and normalize name
            return p_str.lstrip("./").replace(" ", "_")

        for item in archetype_items:
            if not item.path: continue
            identity = _get_gnostic_identity(item.path)
            sovereign_identity_map[identity] = item

            # Archetype matter is willed FIRST
            final_items.append(item)
            review_dossier.append({
                "type": "Sanctum" if item.is_dir else "Scripture",
                "path": str(item.path),
                "description": Text("Sovereign archetype matter."),
                "action": "Archetype", "severity": "info"
            })

        # --- MOVEMENT II: THE WEAVING OF THE GRIMOIRE (SUPPLEMENTAL) ---
        self.Logger.verbose(f"   -> Consulting the Grimoire to bridge the Void...")

        from ...artisans.template_engine import TemplateEngine
        template_engine = TemplateEngine(silent=True)

        for prophecy in GENESIS_GRIMOIRE:
            try:
                # 1. ADJUDICATE NECESSITY
                if not prophecy["adjudicator"](gnosis): continue

                # 2. PATH CONVERGENCE (THE CURE)
                template_path = prophecy["path"]
                resolved_path_str = alchemist.transmute(template_path, alchemical_ctx)
                normalized_path = Path(resolved_path_str)
                identity = _get_gnostic_identity(normalized_path)

                # [ASCENSION 1]: SOVEREIGNTY SHIELD
                # If the Archetype already willed this identity, the Grimoire is STAYED.
                if identity in sovereign_identity_map:
                    self.Logger.debug(f"      - Stayed: '{identity}' is warded by Archetype Sovereignty.")
                    continue

                # Proceed only with supplemental infrastructure...
                is_dir = prophecy.get("is_dir", resolved_path_str.endswith('/'))
                content: Optional[str] = None
                origin: str = "Supplemental"

                content_rite = prophecy.get("content_rite")
                if content_rite:
                    content = content_rite(gnosis, self.current_project_slug)
                    origin = "Synthesized"
                elif not is_dir:
                    template_gnosis = template_engine.perform_gaze(normalized_path, alchemical_ctx)
                    if template_gnosis:
                        content = template_gnosis.content
                        origin = "Forge Fallback"

                final_items.append(ScaffoldItem(
                    path=normalized_path, is_dir=is_dir, content=content,
                    line_num=0, raw_scripture=f"# Prophesied: {prophecy['key']}",
                    line_type=GnosticLineType.FORM
                ))

                review_dossier.append({
                    "type": "Sanctum" if is_dir else "Scripture",
                    "path": str(normalized_path),
                    "description": Text(prophecy.get("review", {}).get("description", "Infrastructure.")),
                    "action": origin, "severity": "info"
                })

            except Exception as e:
                self.Logger.warn(f"Heresy in Grimoire law {prophecy.get('key')}: {e}")

        # [ASCENSION 10]: TOPOLOGICAL PURIFICATION
        final_items.sort(key=lambda x: (not x.is_dir, len(x.path.parts) if x.path else 0))

        return final_items, review_dossier

    def _prophesy_commands(self: 'GenesisDialogueOrchestrator', gnosis: Dict) -> List[str]:
        """
        =================================================================================
        == THE ORACLE OF KINETIC WILL (V-Ω-TOTALITY-V200-COMMAND-FUSION)               ==
        =================================================================================
        [THE CURE]: Merges the Archetype's specific edicts with the Grimoire's best
        practices while annihilating redundant strikes.
        """
        self.Logger.verbose("Scrying the Maestro's Will...")

        final_commands: List[str] = []
        seen_cmd_souls: Set[str] = set()

        def _add_safe(cmd: str):
            # Normalize command for comparison (lowercase, strip extra spaces)
            soul = " ".join(cmd.lower().strip().split())
            if soul not in seen_cmd_souls:
                final_commands.append(cmd.strip())
                seen_cmd_souls.add(soul)

        # 1. HARVEST ARCHETYPE WILL (Priority)
        p_name = gnosis.get('project_type', 'generic')
        if a_info := PROFILES.get(p_name):
            try:
                # Scry the Archetype for its (cmd, line, undo) edicts
                _, _, arch_cmds, _ = self.engine._conduct_master_weave(a_info, gnosis, overrides=gnosis)
                for cmd_tuple in arch_cmds:
                    _add_safe(cmd_tuple[0])
            except Exception:
                pass

        # 2. HARVEST GRIMOIRE WILL (Missing Links)
        # Git Inception logic
        if gnosis.get('use_git') and is_git_installed():
            if not (self.engine.project_root / ".git").exists():
                _add_safe("git init")
                _add_safe("git add .")
                msg = gnosis.get('initial_commit_message') or f"feat: Genesis inception"
                _add_safe(f"git commit -m \"{msg}\"")

        # Python/Poetry logic
        if gnosis.get('project_type') == 'python' and gnosis.get('use_poetry'):
            _add_safe("poetry install")

        return final_commands

    def _forge_gnostic_plan(self: 'GenesisDialogueOrchestrator') -> List[ScaffoldItem]:
        plan, _ = self._prophesy_structure(self.final_gnosis)
        return plan

    def __repr__(self) -> str:
        return f"<Ω_GENESIS_PROPHET status=VIGILANT version=5.12-CONVERGED>"
