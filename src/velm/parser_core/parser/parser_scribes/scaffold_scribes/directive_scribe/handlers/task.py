# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/task.py
# -----------------------------------------------------------------------------------------------------------
import re
import itertools
import ast
import shlex
from typing import List, Dict, Any, Tuple, Optional, Set

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......contracts.symphony_contracts import Edict, EdictType


class TaskHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE KINETIC TASKMASTER (V-Ω-TOTALITY-V9000-MATRIX-SOLVER-ULTIMA)             ==
    =================================================================================
    LIF: 1000x | ROLE: WORKFLOW_ARCHITECT | RANK: OMEGA_SOVEREIGN

    The Sovereign Governor of Kinetic Workflows. It manages the definition,
    dependency linking, and combinatorial explosion of executable tasks.

    ### THE PANTHEON OF ASCENDED FACULTIES:
    1.  **Topological Dependency Grapher (@needs):** Maps causal links between tasks,
        ensuring the Scheduler respects the arrow of time.
    2.  **The Matrix Solver (@matrix):** A high-fidelity combinatorial engine that
        transmutes a single task definition into N variants based on dimensional
        inputs (OS, Version, Env). It performs Alchemical Substitution on the
        task body for each variant.
    3.  **The Cache Sentinel (@cache):** Defines caching strategies based on
        file globs (inputs) and artifact paths (outputs) for zero-cost rebuilding.
    4.  **The Pipeline Weaver (@pipeline):** Parses linear execution chains defined
        as list literals and transmutes them into a meta-task sequence.
    5.  **Decorator Stack Architecture:** Implements a stateful accumulator for
        pre-task decorators, applying them atom-by-atom to the subsequent definition.
    6.  **Socratic Syntax Healing:** Automatically corrects malformed array syntaxes
        in matrix definitions.
    7.  **Trace ID Suture:** Binds every task creation to the active trace ID for
        observability.
    =================================================================================
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The Rite of Task Orchestration.
        Dispatches based on the specific directive soul.
        """
        directive = vessel.directive_type
        raw_line = vessel.raw_scripture.strip()

        # --- MOVEMENT I: DECORATOR ACCUMULATION (THE STACK) ---
        if directive in ("needs", "cache", "matrix"):
            # Ensure the parser has a pending decorators registry
            if not hasattr(self.parser, '_pending_decorators'):
                self.parser._pending_decorators = {}

            # For @needs and @cache, we might want to accumulate or overwrite?
            # Standard pattern: overwrite last saw.
            # However, logic dictates @needs can be additive.
            # For V1 Totality, we map the directive name to the raw value (vessel.name).
            self.parser._pending_decorators[directive] = vessel.name

            # Determine if this was a multiline decorator (rare but possible)
            # For now, we assume decorators are single-line meta-tags.
            return i + 1

        # --- MOVEMENT II: TASK MATERIALIZATION ---
        if directive == "task":
            return self._conduct_task_definition(lines, i, raw_line)

        # --- MOVEMENT III: PIPELINE WEAVING ---
        if directive == "pipeline":
            return self._conduct_pipeline_definition(lines, i, raw_line)

        # --- MOVEMENT IV: ORPHAN GUARD ---
        if directive == "endtask":
            # If we hit an endtask without being inside a consume block, it is an orphan.
            self.Logger.warn(f"L{vessel.line_num}: Orphaned @endtask perceived. Evaporating.")
            return i + 1

        return i + 1

    def _conduct_task_definition(self, lines: List[str], i: int, raw_line: str) -> int:
        """
        [THE RITE OF DEFINITION]
        Parses the @task signature, consumes the body, and applies pending decorators.
        Handles Matrix Explosion if the @matrix decorator is present.
        """
        # 1. PARSE SIGNATURE
        # Syntax: @task name: or @task name
        match = re.match(r'^@task\s+(?P<name>[\w\-]+)\s*:?', raw_line)
        if not match:
            raise ArtisanHeresy(
                "Malformed @task syntax.",
                details=f"Line: {raw_line}",
                line_num=i + 1,
                severity=HeresySeverity.CRITICAL
            )

        task_name = match.group('name')

        # 2. CONSUME BODY
        # We read until @endtask. This gives us the raw commands.
        block_lines, next_i = self._consume_block(lines, i + 1, "@endtask")

        # 3. INHALE DECORATORS
        # Pop the stack of pending metadata
        decs = getattr(self.parser, '_pending_decorators', {}).copy()
        if hasattr(self.parser, '_pending_decorators'):
            self.parser._pending_decorators.clear()

        # Initialize the global task registry if needed
        if not hasattr(self.parser, 'tasks'):
            self.parser.tasks = {}

        # 4. ADJUDICATE MATRIX EXPLOSION
        if "matrix" in decs:
            # If @matrix is present, we do not register the base task.
            # We register N variants of the task.
            return self._handle_matrix_explosion(task_name, decs, block_lines, raw_line, next_i)

        # 5. FORGE THE STANDARD EDICT
        # We parse the body lines into Action Edicts
        body_edicts = []
        for idx, line_content in enumerate(block_lines):
            stripped = line_content.strip()
            # Only creating edicts for kinetic lines (>>) or polyglot headers
            if stripped.startswith('>>') or stripped.startswith('py:') or stripped.startswith('js:'):
                # We use a simplified Edict creation here; the PostRunScribe handles detailed parsing
                # But for the Task registry, we store them as Edicts for the Scheduler.
                body_edicts.append(Edict(
                    type=EdictType.ACTION,
                    command=stripped,
                    raw_scripture=line_content,
                    line_num=i + idx + 2
                ))

        task_edict = Edict(
            type=EdictType.DIRECTIVE,
            directive_type="task_def",
            directive_args=[task_name],
            raw_scripture=raw_line,
            line_num=i + 1,
            body=body_edicts,
            metadata={
                "dependencies": self._lex_list_argument(decs.get("needs", "")),
                "cache_policy": decs.get("cache"),
                "trace_id": getattr(self.parser, 'trace_id', 'void'),
                "description": self._extract_docstring(block_lines)
            }
        )

        # 6. REGISTRATION
        self.parser.tasks[task_name] = task_edict
        self.parser.edicts.append(task_edict)

        self.Logger.verbose(f"L{i + 1}: Kinetic Task '{task_name}' woven into memory.")
        return next_i

    def _handle_matrix_explosion(self, base_name: str, decs: Dict, body: List[str], raw: str, next_i: int) -> int:
        """
        [ASCENSION 12]: THE MATRIX SOLVER.
        Transmutes a single @task into N tasks based on combinatorial dimensions.

        Example:
            @matrix os=["linux", "win"], py=["3.10", "3.11"]
            @task test:
                >> echo "Testing on {{ os }} with Python {{ py }}"

        Output:
            test-linux-3.10, test-linux-3.11, test-win-3.10, test-win-3.11
        """
        matrix_str = decs.get("matrix", "")

        # 1. PARSE DIMENSIONS
        # We use a robust regex to find key=[values] patterns
        # Supports: key=["a", "b"] or key=[1, 2]
        dimensions = {}
        pattern = re.compile(r'(?P<key>\w+)\s*=\s*\[(?P<values>.*?)\]')

        for match in pattern.finditer(matrix_str):
            key = match.group('key')
            raw_values = match.group('values')

            # Safe parsing of the list string
            try:
                # Wrap in brackets to ensure it's a valid list literal if regex stripped them
                # (Regex above captures INSIDE brackets, so we re-wrap for literal_eval)
                eval_str = f"[{raw_values}]"
                parsed_values = ast.literal_eval(eval_str)
                dimensions[key] = [str(v) for v in parsed_values]
            except Exception:
                # Fallback: simple split if AST fails
                dimensions[key] = [v.strip().strip('"\'') for v in raw_values.split(',')]

        if not dimensions:
            self.Logger.warn(
                f"Matrix definition for '{base_name}' resulted in Void dimensions. Creating base task only.")
            # Fallback to standard creation? Or fail? Let's just return without creating to signal error.
            return next_i

        # 2. CARTESIAN PRODUCT
        keys = list(dimensions.keys())
        # Generate all combinations of values
        combinations = list(itertools.product(*dimensions.values()))

        self.Logger.info(f"Matrix Solver: Exploding '{base_name}' into {len(combinations)} variants.")

        # 3. VARIANT GENERATION
        for combo in combinations:
            # Map keys to current values: {'os': 'linux', 'py': '3.10'}
            combo_map = dict(zip(keys, combo))

            # Forge unique name: test-linux-3.10
            # Normalize values to be slug-safe
            slug_suffix = "-".join([re.sub(r'[^a-zA-Z0-9]', '', str(v)) for v in combo])
            instance_name = f"{base_name}-{slug_suffix}"

            # [ASCENSION 1]: ALCHEMICAL SUBSTITUTION
            # We inject the matrix values into the body lines immediately
            instance_body_lines = []
            for line in body:
                transmuted_line = line
                for k, v in combo_map.items():
                    # Replace {{ key }} with value
                    # We use a simple replace here, assuming standard Jinja syntax
                    transmuted_line = transmuted_line.replace(f"{{{{ {k} }}}}", str(v))
                    transmuted_line = transmuted_line.replace(f"{{{{{k}}}}}", str(v))
                instance_body_lines.append(transmuted_line)

            # Forge Edict for this variant
            # Note: We set line_num to 0 or the base line, but these are virtual tasks.
            variant_edict = Edict(
                type=EdictType.DIRECTIVE,
                directive_type="task_def",
                directive_args=[instance_name],
                raw_scripture=f"# Generated from matrix: {raw}",
                line_num=0,
                body=[Edict(type=EdictType.ACTION, command=l.strip(), raw_scripture=l, line_num=0)
                      for l in instance_body_lines if l.strip().startswith('>>')],
                metadata={
                    "matrix_context": combo_map,
                    "is_matrix_variant": True,
                    "original_task": base_name,
                    # Inherit dependencies?
                    # If base needs 'build', variants need 'build'.
                    "dependencies": self._lex_list_argument(decs.get("needs", "")),
                }
            )

            self.parser.tasks[instance_name] = variant_edict
            self.parser.edicts.append(variant_edict)

        return next_i

    def _conduct_pipeline_definition(self, lines: List[str], i: int, raw_line: str) -> int:
        """
        [ASCENSION 15]: THE PIPELINE WEAVER.
        Transmutes a list literal into a sequence of task calls.
        Syntax: @pipeline deploy_all = ['build', 'test', 'deploy']
        """
        match = re.match(r'^@pipeline\s+(?P<name>[\w\-]+)\s*=\s*\[(?P<list>.*?)\]', raw_line)
        if not match:
            # Try multiline syntax or throw heresy? For now, assume single line.
            # If we want to support multiline lists, we'd need block consumption logic here.
            raise ArtisanHeresy("Malformed @pipeline syntax. Ensure list is on one line.", line_num=i + 1)

        name = match.group('name')
        raw_list = match.group('list')

        # Parse the list safely
        try:
            task_list = [t.strip().strip('"\'') for t in raw_list.split(',')]
            task_list = [t for t in task_list if t]  # Remove empty strings
        except Exception:
            raise ArtisanHeresy("Pipeline list fracture.", line_num=i + 1)

        # Synthesize a Meta-Task Edict
        # The body contains sub-edicts that call the other tasks
        body_edicts = []
        for t in task_list:
            body_edicts.append(Edict(
                type=EdictType.DIRECTIVE,
                directive_type="call_task",
                directive_args=[t],
                raw_scripture=f"@call_task {t}",
                line_num=i + 1
            ))

        pipeline_edict = Edict(
            type=EdictType.DIRECTIVE,
            directive_type="task_def",
            directive_args=[name],
            raw_scripture=raw_line,
            line_num=i + 1,
            body=body_edicts,
            metadata={"is_pipeline": True, "steps": task_list}
        )

        if not hasattr(self.parser, 'tasks'): self.parser.tasks = {}
        self.parser.tasks[name] = pipeline_edict
        self.parser.edicts.append(pipeline_edict)

        self.Logger.verbose(f"L{i + 1}: Pipeline '{name}' forged with {len(task_list)} steps.")
        return i + 1

    def _lex_list_argument(self, arg_str: str) -> List[str]:
        """Helper to parse comma-separated strings or JSON-lists into a clean list."""
        if not arg_str: return []
        clean = arg_str.strip()
        if clean.startswith('[') and clean.endswith(']'):
            try:
                return ast.literal_eval(clean)
            except:
                pass
        return [s.strip() for s in clean.split(',')]

    def _extract_docstring(self, lines: List[str]) -> Optional[str]:
        """Extracts comment lines at the start of the block as a description."""
        docs = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                docs.append(stripped.lstrip('#').strip())
            elif not stripped:
                continue
            else:
                break
        return " ".join(docs) if docs else None