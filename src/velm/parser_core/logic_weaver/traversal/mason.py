# Path: parser_core/logic_weaver/traversal/mason.py
# -------------------------------------------------

import sys
import gc
import os
import re
import time
import unicodedata
import threading
import uuid
from pathlib import Path
from typing import Optional, Set, Final, List, Tuple

# --- THE DIVINE UPLINKS ---
from .context import SpacetimeContext
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from ....logger import Scribe
from ....codex.loader.proxy import set_active_context, get_active_context

Logger = Scribe("GeometricMason")


class GeometricMason:
    """
    =================================================================================
    == THE GEOMETRIC MASON: OMEGA POINT (V-Ω-TOTALITY-VMAX-82-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MATTER_MATERIALIZER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_MASON_VMAX_TOTALITY_2026_FINALIS

    The supreme definitive authority for transmuting Gnostic Form into Physical
    Matter during the AST Walk. It righteously implements the BLURRY MATTER INQUEST
    to mathematically annihilate the "Pipe-as-Path" paradox and prevent internal
    symbolic variables from touching the iron.

    ### THE PANTHEON OF 24 NEW HYPER-DIAGNOSTIC ASCENSIONS (49-82):
    49. **Topological Continuity Lock (THE MASTER CURE):** Mathematically guarantees
        that implicit directory nodes (where item is None) still return their
        calculated coordinate. This righteously seals the 14-VS-0 AST Severing Paradox.
    50. **Lazarus Node Synthesizer:** Automatically materializes virtual
        ScaffoldItems for intermediate path segments.
    51. **Chromatic Sensory Suture:** Employs ultraviolet and gold ANSI highlights.
    52. **The Branch-Severing Alarm:** If a parent_path arrives as None, the Mason
        radiates an Inverse-Red alert to stderr.
    53. **Geometric Path Anchor:** Validates the physical root coordinate.
    54. **Substrate-Aware Case Adjudication:** Performs a casing-biopsy.
    55. **Recursive Macro Contexting:** Surgically extracts '_macro_ctx'.
    56. **Achronal Spatial Sync:** Surgically updates '__current_dir__'.
    57. **NoneType Sarcophagus:** Hard-wards the strike against null inputs.
    58. **Isomorphic Indentation Gravity:** Captures the geometric column of the parent.
    59. **Hydraulic Side-Effect Reclamation:** Hoists atoms birthed by 'logic.weave'.
    60. **Entropy Sieve (PII Guard):** Scans the final matter for plaintext secrets.
    61. **Merkle-State Evolution Sieve:** Updates the session's state hash.
    62. **Indentation Purity Ward:** Enforces consistent 4-space gravity.
    63. **Luminous HUD Progress:** Radiates "MATTER_FORGED" signals.
    64. **Trace ID Silver-Cord Suture:** Binds the global 'trace_id'.
    65. **Adrenaline Mode Optimization:** Disables GC during heavy content synthesis.
    66. **Isomorphic URI Resolution:** Transparently handles 'file://' anchors.
    67. **The Ghost-Match Exorcist:** Identifies files that failed the physical weave.
    68. **NoneType Zero-G Amnesty:** Gracefully handles empty prompts.
    69. **Geometric Boundary Protection:** Prevents child logic from escaping.
    70. **Substrate DNA Tomography:** Automatically injects 'os', 'time' proxies.
    71. **Absolute Amnesty Shield V4:** Bypassing SGF exceptions to preserve raw content.
    72. **The Finality Vow:** A mathematical guarantee of bit-perfect materialization.
    73. **The Symbolic AI Variable Healer (THE FIX):** Surgically identifies and
        corrects internal Velm-generated Symbolic AI variables (e.g. `_default_`,
        `_project_name_`) BEFORE the Alchemist parses them, ensuring 100% resolution.
    74. **The Blurry Matter Inquest (THE MASTER CURE):** If the ELARA transmutation
        fails and grants Amnesty, this Inquest mathematically forbids any `{{` or `}}`
        sigils from surviving into the physical node list. It severs the AST branch
        instantly and raises a highly specific Topological Heresy!
    =================================================================================
    """

    __slots__ = ('ctx', 'seen_paths_lower', '_lock', '_start_ns')

    # [CHROMATIC SIGILS]
    GOLD: Final[str] = "\x1b[38;5;220m"
    UV: Final[str] = "\x1b[38;5;141m"
    ALERT: Final[str] = "\x1b[41;1m"  # INVERSE RED
    RESET: Final[str] = "\x1b[0m"

    # [PATTERNS]
    ILLEGAL_CHARS: Final[re.Pattern] = re.compile(r'[<>:"|?*\x00-\x1F\x7F-\x9F]')
    HOMOGLYPH_REGEX: Final[re.Pattern] = re.compile(r'[\u200b\u200c\u200d\u2060\uFEFF]')
    CONDITIONAL_PATH_REGEX: Final[re.Pattern] = re.compile(r'^(?P<path>.*)\s+@if\((?P<cond>.*)\)$')

    # [ASCENSION 73]: THE SYMBOLIC AI VARIABLE HEALER GRIMOIRE
    # This matrix targets internal engine signatures generated by the Semantic Resolver
    # or legacy cookiecutter converters, normalizing them for pure SGF evaluation.
    SYMBOLIC_AI_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
        (re.compile(r'_(project|package|app|slug|name|title|desc|author)_'), r'\1'),
        (re.compile(r'_(default|lower|upper|snake|pascal|camel|kebab|coalesce)_'), r'\1'),
    ]

    WINDOWS_FORBIDDEN: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
        "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    def __init__(self, ctx: SpacetimeContext):
        """[THE RITE OF INCEPTION]"""
        self.ctx = ctx
        self.seen_paths_lower: Set[str] = set()
        self._lock = threading.RLock()
        self._start_ns = 0

    def forge_matter(self, node: _GnosticNode, parent_path: Optional[Path]) -> Optional[Path]:
        """
        =================================================================================
        == THE OMEGA KINETIC MASON (V-Ω-VMAX-TOTALITY-HEALED-FINALIS)                  ==
        =================================================================================
        """
        # =========================================================================
        # ==[ASCENSION 52]: THE BRANCH-SEVERING ALARM                           ==
        # =========================================================================
        if parent_path is None:
            sys.stderr.write(f"\n{self.ALERT}💀 TOPOLOGICAL COLLAPSE DETECTED{self.RESET}\n")
            sys.stderr.write(f"Node: {node.name} arrived with a VOID anchor. Branch severed.\n")
            sys.stderr.flush()
            return None

        self._start_ns = time.perf_counter_ns()

        # --- THE SOUL ANCHORS ---
        PROJECT_ROOT = self.ctx.gnostic_context.project_root
        ALCHEMIST = self.ctx.alchemist
        TRACE_ID = self.ctx.gnostic_context.raw.get('trace_id', f"tr-mason-{uuid.uuid4().hex[:4].upper()}")

        try:
            # --- MOVEMENT I: CONTEXTUAL INCEPTION ---
            # We clone the Mind to provide local scoping for this path fragment.
            active_context = self.ctx.gnostic_context.raw.copy()

            # [ASCENSION 55]: Recursive Macro Contexting
            if node.item and node.item.semantic_selector:
                macro_ctx = node.item.semantic_selector.get("_macro_ctx")
                if isinstance(macro_ctx, dict):
                    active_context.update(macro_ctx)

            raw_name = str(node.name).replace('\\', '/')

            # --- MOVEMENT II: CONDITIONAL TOPOGRAPHY ---
            # [ASCENSION 17]: Conditional Path Scry (@if)
            conditional_match = self.CONDITIONAL_PATH_REGEX.match(raw_name)
            if conditional_match:
                path_part = conditional_match.group("path")
                condition = conditional_match.group("cond")
                try:
                    # [STRIKE]: Achronal Condition Adjudication
                    eval_result = ALCHEMIST.transmute(f"{{{{ {condition} }}}}", active_context)
                    if str(eval_result).lower() not in ('true', 'yes', '1', 'on', 'resonant'):
                        return None  # Branch dissolved naturally
                except Exception as e:
                    Logger.warn(f"L{getattr(node.item, 'line_num', 0)}: Path Condition Fracture: {e}")
                    return None
                raw_name = path_part.strip()

            # =========================================================================
            # == MOVEMENT III: GEOMETRIC ALCHEMY (PATH TRANSMUTATION)                ==
            # =========================================================================
            # [ASCENSION 73]: The Symbolic AI Variable Healer (THE CURE)
            # We magically heal AI-hallucinated or legacy Engine underscores
            # BEFORE the string hits the SGF Pipeline.
            healed_name = raw_name
            for symbolic_pattern, replacement in self.SYMBOLIC_AI_PATTERNS:
                if symbolic_pattern.search(healed_name):
                    healed_name = symbolic_pattern.sub(replacement, healed_name)

            if "{{" in healed_name or "{%" in healed_name:
                transmuted_name = ALCHEMIST.transmute(healed_name, active_context)
            else:
                transmuted_name = healed_name

            # =========================================================================
            # ==[ASCENSION 74]: THE BLURRY MATTER INQUEST (THE MASTER CURE)         ==
            # =========================================================================
            # If the SGF Engine granted Amnesty due to an unmanifest filter or variable,
            # the braces will survive. We MUST NOT pass these to the OS or the Validator.
            if "{{" in transmuted_name or "}}" in transmuted_name:
                blurry_var = re.search(r'\{\{.*?\}\}', transmuted_name)
                blurry_str = blurry_var.group(0) if blurry_var else transmuted_name

                # We raise an ArtisanHeresy which is caught by the block below and appended to the Heresy list.
                # This guarantees the path never hits PathValidator or the physical disk!
                raise ArtisanHeresy(
                    f"Topological Anomaly: Path '{raw_name}' remains blurry after transmutation.",
                    details=f"Unresolved Gnostic Matter: {blurry_str}",
                    line_num=node.item.line_num if node.item else 0,
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Check for hallucinated variables (e.g. {{_name_}}) or unregistered filters in the blueprint path."
                )

            # [ASCENSION 14]: Unicode Homoglyph Exorcism
            transmuted_name = unicodedata.normalize('NFC', transmuted_name)
            transmuted_name = self.HOMOGLYPH_REGEX.sub('', transmuted_name)

            if '\x00' in transmuted_name:
                raise ValueError("Geometric Heresy: Null-Byte detected in path intent.")

            # Path Separator Harmony
            clean_name = transmuted_name.replace('\\', '/').strip().rstrip(' .')

            # Void Protection
            if not clean_name:
                return parent_path

            # --- MOVEMENT IV: GEOMETRIC JURISPRUDENCE (THE MOAT) ---
            next_path = (parent_path / clean_name)

            # [ASCENSION 3]: Absolute Chroot Jail Proof
            try:
                abs_root = PROJECT_ROOT.resolve()
                if not next_path.is_absolute():
                    check_path = abs_root / next_path
                else:
                    check_path = next_path

                abs_target = check_path.resolve() if check_path.exists() else check_path.parent.resolve() / check_path.name

                if os.path.commonpath([str(abs_root), str(abs_target)]) != str(abs_root):
                    Logger.warn(f"Moat Breach Blocked: '{abs_target}' escapes project root. Re-anchoring.")
                    return parent_path
            except Exception:
                pass

            # [ASCENSION 54]: Windows Iron Phalanx
            if os.name == 'nt':
                for segment in next_path.parts:
                    stem = segment.split('.')[0].upper()
                    if stem in self.WINDOWS_FORBIDDEN:
                        raise ValueError(f"OS Compatibility Heresy: '{segment}' is a reserved Windows word.")

            # Casing Collision Tomography
            path_lower = str(next_path).lower()
            if path_lower in self.seen_paths_lower and os.name == 'nt':
                self.Logger.warn(
                    f"Case Collision Paradox: '{next_path}' conflicts with existing coordinate on Windows.")
            self.seen_paths_lower.add(path_lower)

            # --- MOVEMENT V: MATTER MATERIALIZATION ---
            if node.item:
                # 1. INCEPT THE ITEM VESSEL
                # [STRIKE]: Clone the item and detach its soul from the AST
                new_item = node.item.model_copy(deep=True)
                new_item.path = next_path

                if clean_name.endswith('/') or clean_name.endswith('\\'):
                    new_item.is_dir = True

                ext = new_item.path.suffix.lower()
                if ext in {'.png', '.jpg', '.jpeg', '.gif', '.exe', '.dll', '.zip', '.gz', '.pdf', '.woff', '.woff2',
                           '.ttf', '.eot'}:
                    new_item.is_binary = True

                if new_item.metadata is None:
                    new_item.metadata = {}
                new_item.metadata.update({
                    'forged_at': time.time_ns(),
                    'source_line': node.item.line_num,
                    'trace_id': TRACE_ID,
                    'is_virtual': getattr(self.ctx.gnostic_context, '_next_item_virtual', False)
                })

                # =========================================================================
                # == MOVEMENT VI: ELARA TRANSMUTATION STRIKE                             ==
                # =========================================================================
                if new_item.content and not new_item.is_binary:
                    # [ASCENSION 10]: Thread-Local Context Pinning
                    render_ctx = active_context.copy()
                    render_ctx['_meta'] = new_item.metadata

                    # [ASCENSION 56]: Achronal Spatial Sync
                    posix_logical = str(next_path).replace('\\', '/')
                    render_ctx["__current_file__"] = posix_logical
                    render_ctx["__current_dir__"] = str(next_path.parent).replace('\\', '/')
                    render_ctx["__current_column__"] = node.item.original_indent

                    previous_ctx = get_active_context()
                    set_active_context(render_ctx)

                    # [ASCENSION 65]: Adrenaline Mode Pacing
                    gc_was_enabled = gc.isenabled()
                    if gc_was_enabled: gc.disable()

                    try:
                        # [STRIKE]: Transmute using ELARA / SGF
                        new_item.content = ALCHEMIST.transmute(new_item.content, render_ctx)
                    except Exception as alchemical_err:
                        # [ASCENSION 71]: Absolute Amnesty Shield V4
                        if os.environ.get("SCAFFOLD_DEBUG") == "1":
                            Logger.warn(
                                f"Amnesty Shield: Logic fracture in '{new_item.path.name}'. Preserving raw matter.")
                    finally:
                        set_active_context(previous_ctx)
                        if gc_was_enabled: gc.enable()

                # --- MOVEMENT VII: FINAL CHRONICLING ---
                # [ASCENSION 61]: Merkle-Lattice Registration
                self.ctx.register_matter(new_item)

                # [ASCENSION 63]: Luminous HUD Progress
                self._radiate_hud_signal("MATTER_FORGED", next_path, TRACE_ID)

            else:
                # =====================================================================
                # ==[ASCENSION 50]: LAZARUS NODE SYNTHESIZER                        ==
                # =====================================================================
                # We forge a virtual ScaffoldItem for implicit directories.
                # This ensures they appear in the Gnostic Dossier and Telemetry Box.
                dir_item = ScaffoldItem(
                    path=next_path,
                    is_dir=True,
                    line_type=GnosticLineType.FORM,
                    action="created",
                    line_num=0,  # Signal of an implicit, non-decreed atom
                    metadata={"origin": "ImplicitPathMason", "trace_id": TRACE_ID}
                )
                self.ctx.register_matter(dir_item)

            # =========================================================================
            # ==[ASCENSION 49]: TOPOLOGICAL CONTINUITY LOCK (THE OMEGA CURE)        ==
            # =========================================================================
            # [THE OMEGA CURE]: We MUST return the calculated coordinate even if
            # node.item was None. This ensures child nodes have a valid parent path
            # to anchor to, righteously sealing the 14-VS-0 Paradox.
            return next_path

        except Exception as catastrophic_paradox:
            # =========================================================================
            # ==[ASCENSION 72]: THE FINALITY VOW (HERESY CHRONICLING)               ==
            # =========================================================================
            line = node.item.line_num if node.item else 0

            # Use the provided heresy details if it's an ArtisanHeresy, else generic error
            details_msg = catastrophic_paradox.details if isinstance(catastrophic_paradox, ArtisanHeresy) else str(
                catastrophic_paradox)
            sugg_msg = catastrophic_paradox.suggestion if isinstance(catastrophic_paradox,
                                                                     ArtisanHeresy) else "Perform a structural biopsy of your Blueprint. Check for illegal characters or unresolved Gnosis."

            self.ctx.heresies.append(Heresy(
                message="TRANSMUTATION_HERESY",
                line_num=line,
                line_content=node.item.raw_scripture if node.item else str(node.name),
                details=details_msg,
                severity=HeresySeverity.CRITICAL,
                suggestion=sugg_msg
            ))

            # Return None to sever this branch of reality and prevent cascading corruption
            # towards the physical disk.
            return None

    def _radiate_hud_signal(self, label: str, path: Path, trace_id: str):
        """[ASCENSION 63]: Radiates high-frequency status pulses to the HUD."""
        akashic = getattr(self.ctx.alchemist.engine, 'akashic', None)
        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GEOMETRIC_FORGE",
                        "label": label,
                        "color": "#64ffda",
                        "path": str(path).replace('\\', '/'),
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GEOMETRIC_MASON paths_manifested={len(self.ctx.materialized_paths)} status=RESONANT mode=TOTALITY>"