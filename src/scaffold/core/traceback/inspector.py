# scaffold/core/traceback/inspector.py

import inspect
import os
import sys
import linecache
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import is_dataclass, asdict

from .contracts import GnosticFrame, GnosticError
from ...logger import Scribe

# Try to import pydantic for deep inspection
try:
    from pydantic import BaseModel

    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False

Logger = Scribe("ForensicInquisitor")


class StackInspector:
    """
    =================================================================================
    == THE FORENSIC INQUISITOR (V-Ω-STACK-WALKER-ULTIMA)                           ==
    =================================================================================
    LIF: 10,000,000,000,000

    It walks the stack of a fallen program, extracting not just code, but *meaning*.
    It freezes time, capturing source code, variable states, and architectural context.
    """

    def __init__(self):
        self.scaffold_root = Path(__file__).parent.parent.parent.parent.resolve()
        self.cwd = Path.cwd()
        self._recursion_depth = 0

    def inspect_exception(self, exc: BaseException, project_root: Optional[Path] = None) -> GnosticError:
        """
        The Grand Rite of Inspection.
        Transmutes a raw Exception into a GnosticError dossier.
        """
        self.cwd = project_root or self.cwd

        # 1. Walk the Chain (Cause/Context)
        # For V1, we focus on the active traceback, but we could recurse here.
        # We extract the traceback object.
        tb = exc.__traceback__

        # 2. Walk the Stack
        frames = self._walk_stack(tb)

        # 3. Collapse Recursion
        frames = self._collapse_recursion(frames)

        # 4. Capture Context
        active_rite = "Unknown"
        session_id = "Unknown"

        # Try to find the active request in the stack
        for frame in frames:
            if 'request' in frame.locals and isinstance(frame.locals['request'], dict):
                # It's a serialized request dict
                active_rite = frame.locals['request'].get('command', 'Unknown')
                session_id = frame.locals['request'].get('session_id', 'Unknown')
                break
            # Or a Pydantic object
            if 'request' in frame.locals and hasattr(frame.locals['request'], 'command'):
                active_rite = str(getattr(frame.locals['request'], 'command'))

        return GnosticError(
            exc_type=type(exc).__name__,
            exc_value=str(exc),
            timestamp=str(sys.modules.get("time", {}).get("time", "")),  # Placeholder
            frames=frames,
            active_rite=active_rite,
            project_root=str(self.cwd),
            session_id=session_id,
            polyglot_context=None  # Future: Pull from dedicated var
        )

    def _walk_stack(self, tb) -> List[GnosticFrame]:
        frames = []
        while tb:
            frame = tb.tb_frame
            info = inspect.getframeinfo(frame, context=5)  # Capture 5 lines context

            # 1. Path Geometry
            filename = info.filename
            abs_path = Path(filename).resolve()
            try:
                rel_path = abs_path.relative_to(self.cwd)
                display_path = str(rel_path)
            except ValueError:
                display_path = str(abs_path)

            # 2. Identify Gnostic Context
            is_scaffold = str(self.scaffold_root) in str(abs_path)
            is_library = "site-packages" in str(abs_path) or "dist-packages" in str(abs_path)

            comp_type = "System"
            comp_name = ""

            if is_scaffold:
                if "artisans" in str(abs_path):
                    comp_type = "Artisan"
                elif "middleware" in str(abs_path):
                    comp_type = "Middleware"
                elif "core" in str(abs_path):
                    comp_type = "Kernel"

                # Try to find the class name (self)
                if 'self' in frame.f_locals:
                    obj = frame.f_locals['self']
                    comp_name = type(obj).__name__

            # 3. Harvest Source Code
            # getframeinfo gets context, but we want it clean
            context_lines = info.code_context or []
            context_start_line = info.lineno - info.index if info.index is not None else info.lineno

            # 4. Capture & Sanitize Variables
            local_vars = self._capture_locals(frame.f_locals)

            # 5. Forge Frame
            gnostic_frame = GnosticFrame(
                filename=display_path,
                abs_path=str(abs_path),
                lineno=tb.tb_lineno,
                name=info.function,
                line_content=context_lines[info.index].strip() if context_lines and info.index is not None else "<?>",
                context_lines=context_lines,
                context_start_lineno=context_start_line,
                locals=local_vars,
                is_scaffold_code=is_scaffold,
                is_library_code=is_library,
                component_type=comp_type,
                component_name=comp_name,
                # Generate clickable link (VS Code format)
                editor_link=f"vscode://file/{abs_path}:{tb.tb_lineno}"
            )
            frames.append(gnostic_frame)
            tb = tb.tb_next

        return frames

    def _capture_locals(self, local_vars: Dict[str, Any]) -> Dict[str, str]:
        """
        [THE VEIL OF SECRETS & THE SOUL READER]
        Captures variables, redacts secrets, and serializes objects intelligently.
        """
        captured = {}
        for k, v in local_vars.items():
            if k.startswith("__"): continue  # Skip magic methods

            # Secret Redaction
            if any(s in k.lower() for s in ['key', 'secret', 'token', 'password', 'auth']):
                captured[k] = "****** [REDACTED] ******"
                continue

            # Object Soul Reading
            try:
                if PYDANTIC_AVAILABLE and isinstance(v, BaseModel):
                    # Dump small models, summarize large ones
                    d = v.model_dump()
                    val_str = str(d) if len(str(d)) < 500 else f"<{v.__class__.__name__} (Complex Model)>"
                elif is_dataclass(v):
                    val_str = str(asdict(v))
                else:
                    val_str = repr(v)

                if len(val_str) > 200:
                    val_str = val_str[:197] + "..."
                captured[k] = val_str
            except:
                captured[k] = "<Unrepresentable>"
        return captured

    def _collapse_recursion(self, frames: List[GnosticFrame]) -> List[GnosticFrame]:
        """
        [THE RECURSION SENTINEL]
        Detects repeating patterns in the stack and collapses them.
        """
        if len(frames) < 10: return frames

        # Simple heuristic: check for repeated (filename, lineno, function) tuples
        signatures = [(f.filename, f.lineno, f.name) for f in frames]

        # Detect cycles?
        # Simplified: If the last 3 frames are identical to the 3 before them...
        # For now, we just look for massive repetition of the same function name

        from collections import Counter
        counts = Counter(f.name for f in frames)
        recursion_suspects = [name for name, count in counts.items() if count > 20]

        if not recursion_suspects:
            return frames

        # If we have deep recursion, we keep the head and tail
        # This is a visual optimization, not a true cycle detection algo
        new_frames = frames[:10]
        new_frames.append(GnosticFrame(
            filename="... [Recursive Singularity] ...",
            abs_path="",
            lineno=0,
            name="RecursionCollapsed",
            line_content=f"{len(frames) - 20} frames hidden",
            context_lines=[],
            context_start_lineno=0,
            locals={},
            is_scaffold_code=True,
            component_type="System",
            component_name="Paradox",
            editor_link=""
        ))
        new_frames.extend(frames[-10:])
        return new_frames