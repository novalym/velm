# // artisans/analyze/completion_codex/conductor.py

import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable, Set

# --- The Divine Summons of the Master Prophets ---
from .scaffold import get_scaffold_completions
from .symphony import get_symphony_completions
from ....logger import Scribe

Logger = Scribe("CompletionConductor")

# [ASCENSION 5] THE CANON CHRONOCACHE
# Persists the schema across requests to annihilate IPC latency.
_introspection_cache: Optional[Dict[str, Any]] = None


class CompletionConductor:
    """
    =================================================================================
    == THE GRAND CONDUCTOR OF GNOSTIC PROPHECY (V-Ω-UNIVERSAL-SINGULARITY)         ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    The Sovereign Logic that governs Autocomplete. It serves both the VS Code Client
    and the Gnostic Cockpit with equal fidelity.

    It enforces the **Law of Sigil Purity**: If a Sigil is invoked, only Gnosis
    relevant to that Sigil shall be proclaimed.

    It enforces the **Law of the Monad**: In `.arch` files, the logic bifurcates
    based on the cursor's position relative to the `%% symphony` horizon.
    """

    def __init__(self, daemon_communion_rite: Callable):
        self.commune_with_daemon = daemon_communion_rite

        # --- THE PANTHEON OF PROPHETS ---
        self.prophet_pantheon: Dict[str, Callable] = {
            "scaffold": get_scaffold_completions,
            "symphony": get_symphony_completions,
            "arch": self._conduct_arch_prophecy,  # [ASCENSION 1] The Monad Geometer
        }

        # Sigils that demand exclusive attention [ASCENSION 4]
        self.exclusive_sigils: Set[str] = {'$', '@', '%', '?', '!'}

    async def _awaken_oracle_and_receive_gnosis(self) -> Dict[str, Any]:
        """
        [ASCENSION 5] THE RITE OF GNOSTIC COMMUNION (Cached).
        Performs a single, atomic plea to the `introspect` Oracle.
        """
        global _introspection_cache
        if _introspection_cache is not None:
            return _introspection_cache

        Logger.verbose("Oracle Gnosis is a void. Communing with the Gnostic Nexus...")
        try:
            response = await self.commune_with_daemon('introspect', {'topic': 'all'})
            if response.get("success"):
                Logger.success("The Oracle has spoken. The Gnostic Canon is now known.")
                _introspection_cache = response.get("data", {})
                return _introspection_cache
            else:
                Logger.error(f"The Oracle's proclamation was profane: {response.get('message')}")
                return {}
        except Exception as e:
            Logger.error("A catastrophic paradox shattered the communion with the Oracle.", ex=e)
            return {}

    async def prophesy(
            self,
            language_id: str,
            line_prefix: str,
            full_content: str,
            project_root: Path,
            # [ASCENSION 3] The Universal Context Bridge
            context: Optional[Dict[str, Any]] = None,
            # [ASCENSION 2] The Cursor Anchor
            cursor_offset: int = -1
    ) -> List[Dict[str, Any]]:
        """
        The one true, public rite. The gateway for the Language Server's plea.
        """
        start_time = time.perf_counter()

        try:
            # --- MOVEMENT I: THE AWAKENING OF THE ORACLE ---
            introspection_data = await self._awaken_oracle_and_receive_gnosis()

            # --- MOVEMENT II: THE GNOSTIC TRIAGE OF THE TONGUE ---
            prophet = self.prophet_pantheon.get(language_id)
            if not prophet:
                # If unknown tongue, we assume it is text and offer no prophecy.
                return []

            # --- MOVEMENT III: THE HARVEST OF VARIABLES ---
            # [ASCENSION 6] The Variable Harvester: Scans live content for $$ definitions.
            all_vars = list(set(re.findall(r'^\s*\$\$\s*([\w_]+)', full_content, re.MULTILINE)))

            # --- MOVEMENT IV: THE INFERENCE OF INTENT ---
            # [ASCENSION 3 & 7] The Universal Context Bridge & Fallback Gaze
            # Extract trigger char from context OR infer from last char of prefix.
            trigger = context.get('triggerCharacter') if context else None

            if not trigger and line_prefix:
                last_char = line_prefix[-1]
                if last_char in self.exclusive_sigils or last_char in ['/', '.', ':']:
                    trigger = last_char

            # [ASCENSION 4] THE SIGIL SHORT-CIRCUIT
            # If the trigger is a known exclusive sigil, we inject it into the context
            # so the Prophets know to STAY THE HAND of the Cartographer.
            enriched_context = (context or {}).copy()
            enriched_context['triggerCharacter'] = trigger

            # --- MOVEMENT V: THE DIVINE DELEGATION ---
            # We bestow the cursor_offset and full_content upon the prophet.
            # Note: Specific prophets must be updated to accept these args or we handle it via **kwargs pattern in them.
            # Our prophet signatures are robust (kwargs or explicit).

            # For the .arch handler, we pass specific arguments.
            if language_id == 'arch':
                suggestions = self._conduct_arch_prophecy(
                    line_prefix=line_prefix,
                    all_vars=all_vars,
                    project_root=project_root,
                    introspection_data=introspection_data,
                    context=enriched_context,
                    full_content=full_content,
                    cursor_offset=cursor_offset
                )
            else:
                suggestions = prophet(
                    line_prefix=line_prefix,
                    all_vars=all_vars,
                    project_root=project_root,
                    introspection_data=introspection_data,
                    context=enriched_context
                )

            # [ASCENSION 10 & 11] Luminous Telemetry & Void Guard
            # Filter None/Empty items and log stats.
            valid_suggestions = [s for s in suggestions if s]

            duration = (time.perf_counter() - start_time) * 1000
            if duration > 100:  # Only log slow prophecies
                Logger.warn(f"Slow Prophecy ({duration:.2f}ms). Items: {len(valid_suggestions)}. Trigger: {trigger}")

            return valid_suggestions

        except Exception as e:
            # [ASCENSION 9] The Unbreakable Ward
            Logger.error(f"Prophecy Failed: {e}", exc_info=True)
            return []

    def _conduct_arch_prophecy(
            self,
            line_prefix: str,
            all_vars: List[str],
            project_root: Path,
            introspection_data: Dict[str, Any],
            context: Optional[Dict[str, Any]] = None,
            full_content: str = "",
            cursor_offset: int = -1
    ) -> List[Dict[str, Any]]:
        """
        [ASCENSION 1] THE MONAD GEOMETER.
        Perceives which reality the Architect is in—Form (.scaffold) or Will (.symphony)—
        within a Unified `.arch` scripture.
        """
        # The Default State is Form (Scaffold)
        use_symphony = False

        # --- MOVEMENT A: THE GEOMETRIC GAZE ---
        # If we have the cursor offset and content, we look for the separator.
        if cursor_offset != -1 and full_content:
            # We search for the sacred separator: `%% symphony`
            match = re.search(r'^(\s*)%%(\s*)symphony', full_content, re.MULTILINE)
            if match:
                # If the cursor is spatially AFTER the separator, we are in the Will.
                if cursor_offset > match.end():
                    use_symphony = True

        # --- MOVEMENT B: THE HEURISTIC FALLBACK ---
        # If geometry fails (no offset), we guess based on the line content.
        else:
            stripped = line_prefix.strip()
            # If the line starts with standard Symphony edicts, assume Symphony.
            if stripped.startswith(('>>', '??', 'py:', 'js:', 'go:', 'rs:', 'sh:')):
                use_symphony = True

        # --- MOVEMENT C: THE DIVINE DELEGATION ---
        if use_symphony:
            # [ASCENSION 7] The Language Fork -> Symphony
            return get_symphony_completions(
                line_prefix=line_prefix,
                all_vars=all_vars,
                project_root=project_root,
                introspection_data=introspection_data,
                context=context
            )
        else:
            # [ASCENSION 7] The Language Fork -> Scaffold (Form)
            return get_scaffold_completions(
                line_prefix=line_prefix,
                all_vars=all_vars,
                project_root=project_root,
                introspection_data=introspection_data,
                context=context
            )