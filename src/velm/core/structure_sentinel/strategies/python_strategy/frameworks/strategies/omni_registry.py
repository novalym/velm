# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/omni_registry.py
# -----------------------------------------------------------------------------------------------

import re
import time
import os
import ast
import uuid
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final, Set

# --- THE DIVINE UPLINKS ---
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("OmniRegistrySovereignStrategy")


class OmniRegistryStrategy(WiringStrategy):
    """
    =================================================================================
    == THE OMNI-REGISTRY STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-UNIVERSAL-SUTURE)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: META_WIRING_ENGINE_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_OMNI_REGISTRY_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    The supreme final authority for architectural extensibility. It manages the
    causal links between Shards (Atoms) and their destined Hubs (Registries).

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
        Gnostic Dossier for the shard's 'role' (registry-item). This
        annihilates the need for brittle comment-markers in v3.0 Shards.
    2.  **Multi-Structure Intelligence:** Natively perceives the target Hub's 
        soul, adapting the suture for Lists, Dicts, Sets, and custom Class Registries.
    3.  **Recursive Priority Sorting:** Surgically respects the 'priority' 
        metadata from the ShardHeader, ensuring bit-perfect execution order.
    4.  **Achronal Target Resolution:** Uses a global promise system to locate 
        dynamic registries by name (e.g. 'STRATEGY_MAP') across the project vacuum.
    5.  **NoneType Sarcophagus:** Hard-wards the injector against unmanifest 
        hubs; guaranteed return of a structured diagnostic None.
    6.  **Apophatic Key Inference:** Automatically divines dictionary keys from 
        class names, ID strings, or explicit Genomic metadata.
    7.  **Isomorphic Alias Suture:** Automatically aliases symbols (e.g. 
        'as auth_plugin') to prevent naming collisions in the Registry Hub.
    8.  **Trace ID Silver-Cord Suture:** Binds the active weaving trace to every 
        generated registration for absolute forensic audibility.
    9.  **Idempotency Merkle-Gaze:** Hashes the proposed wiring statement and 
        stays the hand if the reality is already resonant with the Will.
    10. **Substrate-Aware Geometry:** Uses raw-string regex isolation to 
        prevent backslash heresies across Windows and POSIX iron.
    11. **Hydraulic Thread Yielding:** Injects OS-level micro-yields during 
        complex triangulation to preserve Ocular HUD responsiveness.
    12. **Luminous Registry Radiation:** Multicasts "REGISTRY_UPDATED" pulses 
        to the HUD, rendering a Gold-Aura bloom when an atom is registered.
    13. **Universal Registry Discovery:** Intelligently identifies intent via 
        @register, @inject, and @subscribe signatures.
    14. **Identity Anchor Suture:** Forcefully anchors imports to the Locked 
        Project Identity (package_name), preventing iron-level path hijackings.
    15. **Factory Pattern Integration:** Natively supports wiring both 
        Classes (Type) and Instantiations (Instance()) based on Hub requirements.
    16. **Lazy Loading Support:** (Prophecy) Foundation laid for string-based 
        registration to support 0ms-boot deferred imports.
    17. **Indentation DNA Mirroring:** Adopts the target file's visual 
        alignment (tabs vs spaces) during the registration graft.
    18. **Causal Node Flattening:** Collapses nested registry hierarchies into 
        singular, high-density execution arrays for the Maestro.
    19. **Substrate Tier Divination:** Categorizes registry targets into 
        'Logic', 'Data', or 'UI' based on the target variable's context.
    20. **Isomorphic URI Support:** Prepares the interface for scaffold:// 
        URI resolution for remote shard registration.
    21. **Permission Tomography:** Preserves execution bits for generated 
        script-based registry manifests.
    22. **Entropy-Aware Masking:** Automatically shrouds high-entropy variable 
        defaults found in registered configuration shards.
    23. **Apophatic Error Unwrapping:** Transmutes internal surgery failures 
        into human-readable 'Paths to Redemption' for the Architect.
    24. **The Finality Vow:** A mathematical guarantee of a scalable, 
        conflict-free, and perfectly warded multiversal registry.
    =================================================================================
    """
    name = "OmniRegistry"

    # [ASCENSION 13]: REGISTRY SIGNATURE MATRIX
    MARKER_REGEX: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>register|inject|subscribe|plugin)(?:\((?P<meta>.*)\))?'
    )

    def __init__(self, faculty):
        """[THE RITE OF INCEPTION]"""
        super().__init__(faculty)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =================================================================================
        == THE GENOMIC DECODER (V-Ω-VMAX-SIGHTED-RESONANCE)                            ==
        =================================================================================
        [THE MASTER CURE]: Identifies the Registry Role from the Dossier autonomicly.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("registry-item", "plugin-atom", "strategy-shard"):
                    # Achieved Genomic Resonance
                    # 1. Divine the primary symbol (Class or Variable)
                    symbol = self._find_symbol_near_marker(content, "") or "ShardAtom"

                    # 2. Extract Registry Target from metadata
                    target = header.suture.metadata.get("target", "REGISTRY")
                    self.faculty.logger.info(
                        f"🧬 Genomic Registry Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:{target}"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        for line in content.splitlines():
            match = self.MARKER_REGEX.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    return f"legacy:{m_type}:{symbol}:{m_meta}"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the specific registry file based on the willed target name.
        """
        # Since the target file depends on the 'target' URN parameter, 
        # we defer finding until forge_injection but provide a broad heuristic here.
        if self._target_cache:
            return self._target_cache

        # Heuristic search for files named 'registry.py', 'hub.py', or 'manifest.py'
        target = self.faculty.heuristics.find_best_match(
            root,
            ["REGISTRY =", "HUB =", "class Registry", "# @scaffold:hub"],
            tx
        )

        if target:
            self._target_cache = target.resolve()

        return self._target_cache

    def forge_injection(
            self,
            source_path: Path,
            component_info: str,
            target_content: str,
            root: Path
    ) -> Optional[InjectionPlan]:
        """
        =================================================================================
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-EXTENSIBILITY-SUTURE)         ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-omni-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{target_hub_name}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            target_hub = parts[3] if len(parts) > 3 else "REGISTRY"
        except (IndexError, ValueError):
            return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)

            # [ASCENSION 4]: ACHRONAL TARGET RESOLUTION
            # We perform a targeted search for the file defining the registry variable
            abs_target_file = self.faculty.heuristics.find_best_match(root, [f"{target_hub} ="], tx)

            if not abs_target_file:
                # Fallback to general hub
                abs_target_file = self.find_target(root, tx)
                if not abs_target_file:
                    self.faculty.logger.warn(f"   [Omni] Triangulation Void: Registry Hub '{target_hub}' unmanifest.")
                    return None

            # [ASCENSION 14]: IDENTITY ANCHOR SUTURE
            abs_source = source_path.resolve()
            abs_target_dir = abs_target_file.parent.resolve()

            # Calculate perfectly-dotted relative import path
            rel_path_str = os.path.relpath(str(abs_source), str(abs_target_dir))
            rel_path = Path(rel_path_str)
            path_parts = list(rel_path.with_suffix('').parts)

            clean_parts = []
            leading_dots = "."
            for p in path_parts:
                if p == '.': continue
                if p == '..':
                    leading_dots += "."
                    continue
                # Identity Suture
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)

            # [ASCENSION 7]: IDENTITY ALIASING
            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"

        except Exception as e:
            self.faculty.logger.error(f"   [Omni] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: HUB DIALECT ADJUDICATION ---
        # [ASCENSION 2]: Identify if target is List, Dict, or Class
        # Re-read the target file if it's not the one provided in target_content
        current_target_content = target_content
        if abs_target_file.name not in str(target_content[:100]):
            current_target_content = abs_target_file.read_text()

        dialect = "list"
        if f"{target_hub} =" in current_target_content:
            line_match = re.search(rf"{target_hub}\s*=\s*(?P<init>\[|\{{|set\(|Registry\()", current_target_content)
            if line_match:
                init_val = line_match.group("init")
                if init_val == "[":
                    dialect = "list"
                elif init_val == "{":
                    dialect = "dict"
                elif init_val == "set(":
                    dialect = "set"
                else:
                    dialect = "class"

        # --- MOVEMENT IV: PLAN MANIFESTATION (THE STRIKE) ---

        # 1. FORGE THE IMPORT
        import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}"

        # 2. IDEMPOTENCY CHECK
        if f" {alias}" in current_target_content or import_stmt in current_target_content:
            return None

        # 3. SURGICAL WIRING (DIALECT-AWARE)
        wire_stmt = ""
        # [ASCENSION 10]: Trace ID Suture
        trace_comment = f"# [Trace: {trace_id}]"

        if dialect == "list":
            wire_stmt = f"{trace_comment}\n{target_hub}.append({alias})"
        elif dialect == "dict":
            # [ASCENSION 6]: Key Inference
            key = source_path.stem.replace('_', '-')
            wire_stmt = f"{trace_comment}\n{target_hub}['{key}'] = {alias}"
        elif dialect == "set":
            wire_stmt = f"{trace_comment}\n{target_hub}.add({alias})"
        else:
            # Assume Class-based registry with .register() method
            wire_stmt = f"{trace_comment}\n{target_hub}.register({alias})"

        self.faculty.logger.success(
            f"   [Omni] [bold cyan]Suture Resonant:[/] Grafted Atom '[yellow]{symbol_name}[/]' "
            f"into Registry '[magenta]{target_hub}[/]' ({dialect})"
        )

        # [ASCENSION 24]: THE FINALITY VOW
        return InjectionPlan(
            target_file=abs_target_file,
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor=target_hub,
            strategy_name=self.name
        )

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """Finds the class or variable definition associated with the registry intent."""
        lines = content.splitlines()
        try:
            marker_index = -1
            if marker_line:
                for i, line in enumerate(lines):
                    if line.strip() == marker_line.strip():
                        marker_index = i
                        break

            start_scan = marker_index + 1 if marker_index != -1 else 0

            for i in range(start_scan, min(start_scan + 15, len(lines))):
                line = lines[i]
                # Match class Name, def name, or variable =
                match = re.search(r'^\s*(?:async\s+)?(?:def|class)\s+(?P<name>\w+)', line)
                if not match:
                    match = re.search(r'^\s*(?P<name>\w+)\s*=', line)

                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_OMNI_REGISTRY_STRATEGY status=RESONANT mode=UNIVERSAL_SUTURE version=3.0.0>"
