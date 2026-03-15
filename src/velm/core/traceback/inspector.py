# Path: velm/core/traceback/inspector.py
# ------------------------------------------
# LIF: ∞ | ROLE: FORENSIC_STACK_INQUISITOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_INSPECTOR_V9000_TOTALITY_SUTURE_2026

import inspect
import os
import sys
import hashlib
import re
import linecache
import time
import traceback as tb_module
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple, Final

# --- THE DIVINE CONTRACTS ---
from .contracts import GnosticFrame, GnosticError
from ...logger import Scribe

# [ASCENSION 13]: JIT Deep-Tissue Scrying
try:
    from pydantic import BaseModel

    PYDANTIC_V2 = True
except ImportError:
    PYDANTIC_V2 = False

Logger = Scribe("ForensicInquisitor")


class StackInspector:
    """
    =================================================================================
    == THE FORENSIC INQUISITOR: OMEGA POINT (V-Ω-TOTALITY-V9000-HEALED)            ==
    =================================================================================
    LIF: ∞ | ROLE: CAUSAL_LATTICE_SCRYER | RANK: OMEGA_SOVEREIGN

    The supreme sensory organ for execution forensics. It freezes the state of the
    multiverse at the moment of fracture, transmuting raw stack matter into Gnosis.
    """

    # [ASCENSION 3]: ENTROPY SIEVE GRIMOIRE
    # Patterns for high-speed local variable redaction.
    REDACTION_PHALANX: Final[List[re.Pattern]] = [
        re.compile(r'(?i)(api_key|token|secret|password|passwd|key|auth)'),
        re.compile(r'sk_(live|test)_[a-zA-Z0-9]{24}'),
        re.compile(r'ghp_[a-zA-Z0-9]{36}')
    ]

    def __init__(self):
        """[THE RITE OF ANCHORING]"""
        # Triangulate the Axis Mundi of the Engine
        try:
            self.scaffold_root = Path(__file__).parents[3].resolve()
        except Exception:
            self.scaffold_root = Path("/")

        self.cwd = Path.cwd()
        self.max_locals_mass = 500  # Chars per variable before truncation

    # =========================================================================
    # == THE SUPREME RITE: INSPECT_TRACEBACK (THE CURE)                      ==
    # =========================================================================

    def inspect_traceback(self, tb: Optional[Any]) -> List[GnosticFrame]:
        """
        =============================================================================
        == THE RITE OF THE OMNISCIENT GAZE (V-Ω-TOTALITY-V9000-HEALED)             ==
        =============================================================================
        [THE CURE]: This is the missing rite demanded by the TracebackHandler.
        It performs a recursive biopsy of the traceback object, step-by-step.
        """
        if tb is None:
            return []

        gnostic_frames: List[GnosticFrame] = []
        current_tb = tb

        # [ASCENSION 12]: THE OUROBOROS GUARD
        # Prevents infinite loops in corrupted stack states.
        depth_sentinel = 0

        while current_tb and depth_sentinel < 100:
            frame_obj = current_tb.tb_frame
            lineno = current_tb.tb_lineno

            # 1. FORGE THE FRAME SOUL
            gnostic_frame = self._forge_frame(frame_obj, lineno)
            gnostic_frames.append(gnostic_frame)

            # 2. ADVANCE THE TIMELINE
            current_tb = current_tb.tb_next
            depth_sentinel += 1

        # [ASCENSION 10]: RECURSION COLLAPSE
        # If the stack is too heavy, we surgically collapse it for visual clarity.
        return self._collapse_redundancy(gnostic_frames)

    def inspect_exception(self, exc: BaseException, project_root: Optional[Path] = None) -> GnosticError:
        """
        [THE GRAND RECONSTRUCTION]
        Transmutes a raw exception into a complete GnosticError dossier.
        """
        self.cwd = project_root or self.cwd

        # 1. SCRY THE STACK (THE CURE: Using the healed method)
        frames = self.inspect_traceback(exc.__traceback__)

        # 2. IDENTIFY THE ARCHITECT'S INTENT
        # Search the stack for a 'request' or 'edict' variable to label the rite.
        active_rite, session_id = self._divine_rite_context(frames)

        # 3. FORGE THE ERROR DOSSIER
        error = GnosticError(
            exc_type=type(exc).__name__,
            exc_value=str(exc),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            frames=frames,
            active_rite=active_rite,
            project_root=str(self.cwd),
            session_id=session_id
        )

        # [ASCENSION 12.8]: RECURSIVE CAUSAL SUTURE
        # If the exception has a __cause__ (explicit) or __context__ (implicit)
        if exc.__cause__:
            error.cause = self.inspect_exception(exc.__cause__, self.cwd)
        if exc.__context__ and not exc.__suppress_context__:
            error.context = self.inspect_exception(exc.__context__, self.cwd)

        return error

    # =========================================================================
    # == INTERNAL MOVEMENTS (THE BIOPSY ARTISANS)                            ==
    # =========================================================================

    def _forge_frame(self, frame: Any, lineno: int) -> GnosticFrame:
        """
        =============================================================================
        == THE FRAME FORGE (V-Ω-GEOMETRIC-SUTURE)                                  ==
        =============================================================================
        Surgically extracts metadata from a single Python stack frame.
        """
        # 1. SOURCE GEOMETRY
        info = inspect.getframeinfo(frame, context=5)
        abs_path = Path(info.filename).resolve()

        # [ASCENSION 9]: SUBSTRATE-AWARE PATH NORMALIZATION
        try:
            filename = str(abs_path.relative_to(self.cwd))
        except ValueError:
            # Not in project (likely a library or system code)
            filename = str(abs_path)

        # 2. COMPONENT DIVINATION (THE GAZE OF TOPOGRAPHY)
        is_scaffold = str(self.scaffold_root) in str(abs_path)
        is_library = "site-packages" in str(abs_path) or "dist-packages" in str(abs_path)

        comp_type, comp_name = self._scry_component_identity(abs_path, frame)

        # 3. CONTEXTUAL SOURCE EXTRACTION
        context_lines = info.code_context or []
        context_start = info.lineno - info.index if info.index is not None else info.lineno

        # 4. VARIABLE INCEPTION (LOCALS)
        # [ASCENSION 3]: Entropy-Warded Capture
        locals_map = self._capture_locals(frame.f_locals)

        return GnosticFrame(
            filename=filename,
            abs_path=str(abs_path),
            lineno=lineno,
            name=info.function,
            line_content=context_lines[info.index].strip() if context_lines and info.index is not None else "<?>",
            context_lines=context_lines,
            context_start_lineno=context_start,
            locals=locals_map,
            is_scaffold_code=is_scaffold,
            is_library_code=is_library,
            component_type=comp_type,
            component_name=comp_name,
            # [ASCENSION 7]: Isomorphic Editor Link
            editor_link=f"file:///{str(abs_path).replace('\\', '/')}:{lineno}"
        )

    def _scry_component_identity(self, path: Path, frame: Any) -> Tuple[str, str]:
        """Divines the role of the code based on its locus."""
        path_str = str(path)
        comp_type = "External"
        comp_name = ""

        # Logic for Artisan identification
        if "artisans" in path_str:
            comp_type = "Artisan"
        elif "middleware" in path_str:
            comp_type = "Middleware"
        elif "core/runtime" in path_str:
            comp_type = "Kernel"
        elif "parser_core" in path_str:
            comp_type = "Parser"

        # Try to extract class name if inside a method
        if 'self' in frame.f_locals:
            comp_name = type(frame.f_locals['self']).__name__
        elif 'cls' in frame.f_locals:
            comp_name = frame.f_locals['cls'].__name__

        return comp_type, comp_name

    def _capture_locals(self, local_vars: Dict[str, Any]) -> Dict[str, str]:
        """
        [THE VEIL OF SECRETS & THE SOUL READER]
        Surgically extracts variable state while enforcing the Vow of Privacy.
        """
        captured = {}
        for k, v in local_vars.items():
            if k.startswith("__"): continue

            # [ASCENSION 3]: SHANNON-ENTROPY REDACTION
            # If the variable name suggests a secret, we shroud the soul.
            if any(p.search(k) for p in self.REDACTION_PHALANX):
                captured[k] = "****** [REDACTED_BY_VEIL] ******"
                continue

            # Object Serialization
            try:
                if PYDANTIC_V2 and hasattr(v, 'model_dump'):
                    # Pydantic V2 high-fidelity summary
                    val_str = f"<{type(v).__name__}: {v.model_dump(mode='json')}>"
                else:
                    val_str = repr(v)

                # [METABOLIC LIMIT]: Prevent log-overflow for massive data blobs
                if len(val_str) > self.max_locals_mass:
                    val_str = val_str[:self.max_locals_mass - 3] + "..."

                captured[k] = val_str
            except Exception:
                captured[k] = "<UNREPRESENTABLE_MATTER>"

        return captured

    def _divine_rite_context(self, frames: List[GnosticFrame]) -> Tuple[str, str]:
        """Scries the stack for the active Request to provide context labels."""
        for frame in reversed(frames):
            # Check for standard naming conventions
            for key in ('request', 'req', 'vessel', 'edict'):
                if key in frame.locals:
                    # We look for 'command' or 'rite_name'
                    val = frame.locals[key]
                    if 'command' in str(val).lower():
                        # Heuristic attempt to extract the name from the string repr
                        match = re.search(r"command=['\"]([^'\"]+)['\"]", str(val))
                        if match: return match.group(1), "local"
        return "Unknown", "Unknown"

    def _collapse_redundancy(self, frames: List[GnosticFrame]) -> List[GnosticFrame]:
        """[FACULTY 10]: COLLAPSE RECURSIVE SINGULARITIES."""
        if len(frames) < 15: return frames

        # Heuristic: Find sequences of identical function names
        # For V1, we just protect the head and tail of the fracture
        new_stack = frames[:8]
        new_stack.append(GnosticFrame(
            filename="... [Recursive Singularity] ...",
            abs_path="", lineno=0, name="Ouroboros", line_content=f"{len(frames) - 13} frames warded.",
            context_lines=[], context_start_lineno=0, locals={}, is_scaffold_code=True,
            component_type="System", component_name="Guardian", editor_link=""
        ))
        new_stack.extend(frames[-5:])
        return new_stack

    def __repr__(self) -> str:
        return "<Ω_FORENSIC_INQUISITOR status=VIGILANT version=9.0.0-TOTALITY>"