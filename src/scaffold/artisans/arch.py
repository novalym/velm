# // scaffold/artisans/arch.py
# // -------------------------

import argparse
import tempfile
from pathlib import Path
from typing import Tuple, List

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..core.kernel.transaction import GnosticTransaction
from ..creator import create_structure
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import ArchRequest
from ..parser_core.parser import ApotheosisParser
from ..symphony.conductor import SymphonyConductor


class ArchArtisan(BaseArtisan[ArchRequest]):
    """
    =================================================================================
    == THE ARCH MONAD (V-Ω-UNIFIED-CONDUCTOR)                                      ==
    =================================================================================
    LIF: 10,000,000

    The God-Engine of the Unified Scripture (`.arch`). It orchestrates the atomic
    fusion of Form (Scaffold) and Will (Symphony).
    """

    def execute(self, request: ArchRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE RITE OF THE UNIFIED MONAD (V-Ω-EXECUTE-ULTIMA)                          ==
        =================================================================================
        Conducts the Arch Monad: The atomic fusion of Form (Scaffold) and Will (Symphony).
        """
        import time

        arch_path = Path(request.arch_path).resolve()

        if not arch_path.is_file():
            return self.failure(f"Arch scripture not found at: {arch_path}")

        # 2. The Monad Parser (Split Form/Will)
        form_scripture, will_scripture = self._split_monad(arch_path)

        # 3. The Synthetic Bridge (Legacy Compat)
        synthetic_args = self._forge_synthetic_args(request)

        # --- PHASE I: THE RITE OF FORM (CREATION) ---
        self.logger.info(f"Phase I: Materializing Form from '{arch_path.name}'...")
        start_time = time.monotonic()

        form_parser = ApotheosisParser(grammar_key='scaffold')

        # Parse Form & Resolve Variables
        form_parser.parse_string(
            form_scripture,
            file_path_context=arch_path,
            pre_resolved_vars=request.variables
        )

        # [FIX] THE LAW OF LOGIC RESOLUTION (PARADOX II HEALED)
        # We invoke `resolve_reality` to process Logic items and prune the tree.
        # This prevents Logic tags from being passed to the Creator as files.
        form_items = form_parser.resolve_reality()

        # Commands and variables are retrieved from the parser state
        # Note: form_parser.post_run_commands is List[Tuple[str, int]]. We extract strings.
        form_commands = [cmd for cmd, _ in form_parser.post_run_commands]
        form_variables = form_parser.variables

        created_artifacts: List[Artifact] = []

        # The Transactional Shield
        if not request.dry_run and not request.preview:
            with GnosticTransaction(self.project_root, f"Arch: {arch_path.name}", arch_path, use_lock=True) as tx:
                create_structure(
                    scaffold_items=form_items,
                    post_run_commands=form_commands,
                    base_path=self.project_root,
                    pre_resolved_vars=form_variables,
                    parser_context=form_parser,
                    args=synthetic_args,
                    transaction=tx
                )
                # Harvest Artifacts
                for res in tx.write_dossier:
                    created_artifacts.append(Artifact(
                        path=res.path,
                        type="file",
                        action=res.action_taken,
                        size_bytes=res.bytes_written,
                        checksum=res.gnostic_fingerprint
                    ))
        else:
            # Simulation Mode
            create_structure(
                scaffold_items=form_items,
                post_run_commands=form_commands,
                base_path=self.project_root,
                pre_resolved_vars=form_variables,
                parser_context=form_parser,
                args=synthetic_args
            )

        # The Simulation Guard (Early Exit)
        if (request.preview or request.dry_run) and not request.force:
            self.logger.info("Prophecy of Form complete. The Symphony of Will remains dormant in simulation.")
            return self.success(
                "Arch simulation complete.",
                artifacts=created_artifacts,
                data={"variables": form_variables}
            )

        # --- PHASE II: THE RITE OF WILL (VERIFICATION) ---
        self.logger.info("Phase II: Awakening the Symphony Conductor...")

        # The Ephemeral Scripture
        # We write the Will portion to a temp file so the Conductor can read it properly.
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.symphony', encoding='utf-8') as tmp_symphony:
            tmp_symphony.write(will_scripture)
            tmp_symphony_path = Path(tmp_symphony.name)

        try:
            # The Conductor
            conductor = SymphonyConductor(
                symphony_path=tmp_symphony_path,
                cli_args=synthetic_args,
                execution_root=self.project_root
            )

            # [ELEVATION 2] The Gnostic Bridge
            # We inject the variables resolved from the Blueprint (Phase I) into the Symphony (Phase II).
            # This allows the script to use $$ variables defined in the scaffold part.
            conductor.context.update(form_variables)

            # Execute
            conductor.conduct()

        except Exception as e:
            # If Will fails, we raise Heresy.
            # Note: If Phase I was transactional, it has already committed.
            raise ArtisanHeresy(f"The Symphony of Will faltered: {e}", child_heresy=e)
        finally:
            # The Clean-Up Guarantee
            if tmp_symphony_path.exists():
                try:
                    tmp_symphony_path.unlink()
                except OSError:
                    pass

        # --- FINAL PROCLAMATION ---
        duration = time.monotonic() - start_time
        return self.success(
            f"The Arch Monad '{arch_path.name}' has been fully realized in {duration:.2f}s.",
            artifacts=created_artifacts,
            data={"variables": form_variables}
        )

    def _split_monad(self, path: Path) -> Tuple[str, str]:
        """
        =================================================================================
        == THE MONAD PARSER (V-Ω-REGEX-SENTINEL)                                       ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000

        Performs the **Rite of Bifurcation** upon the `.arch` scripture. It separates
        the **Form** (Scaffold Blueprint) from the **Will** (Symphony Script).
        """
        import re

        # 1. The Rite of Reading
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            raise ArtisanHeresy(f"Could not read the Monad scripture at '{path}': {e}")

        # 2. The Gnostic Regex (The Separator)
        # Matches: Start of line, '%%', optional space, 'symphony', optional space, optional comment, end of line.
        separator_pattern = re.compile(r'(?m)^%%\s*symphony\s*(?:#.*)?$')

        # 3. The Search for the Boundary
        match = separator_pattern.search(content)

        if not match:
            raise ArtisanHeresy(
                "Structural Heresy: The Monad is indivisible.",
                details=f"The scripture '{path.name}' lacks the sacred separator.",
                suggestion="Insert '%% symphony' on a new line to separate Form (Blueprint) from Will (Script)."
            )

        # 4. The Rite of Bifurcation
        split_index = match.start()
        end_index = match.end()

        # Extract Form (Before) and Will (After)
        form_scripture = content[:split_index]
        will_scripture = content[end_index:]

        # 5. The Whitespace Purification
        clean_form = form_scripture.strip()
        clean_will = will_scripture.strip()

        # 6. The Void Sentinel (Telemetry)
        if not clean_form:
            self.logger.verbose(f"Monad '{path.name}' possesses no Form (Scaffold).")
        if not clean_will:
            self.logger.verbose(f"Monad '{path.name}' possesses no Will (Symphony).")

        # 7. The Lineage Tracer
        # Calculate the line number where the split occurred for debugging context
        split_line_num = content.count('\n', 0, split_index) + 1
        self.logger.verbose(f"Bifurcation occurred at line {split_line_num}.")

        return clean_form, clean_will

    def _forge_synthetic_args(self, request: ArchRequest) -> argparse.Namespace:
        """
        =================================================================================
        == THE SYNTHETIC BRIDGE (V-Ω-ADAPTER-PATTERN. THE NECESSARY EVIL)              ==
        =================================================================================
        LIF: 10,000,000

        Forges a `argparse.Namespace` object from the pure `ArchRequest`.
        """
        # --- MOVEMENT I: THE ALCHEMY OF VARIABLES ---
        # Legacy parsers expect variables as a list of strings ["key=value", "key2=val2"].
        # We must transmute our pure Dictionary back into this primitive form.
        # We explicitly cast values to strings to ensure serialization safety.
        set_vars = [f"{k}={str(v)}" for k, v in request.variables.items()]

        # --- MOVEMENT II: THE FORGING OF THE NAMESPACE ---
        return argparse.Namespace(
            # === CORE IDENTITY ===
            # The root must be a string for the legacy `os.path` calls inside the engines.
            root=str(self.project_root),

            # === THE DUAL-KEY VARIABLE BINDING ===
            # Scaffold Engine looks for 'set'. Symphony Engine looks for 'var'.
            # We populate both to ensure universal compatibility across the Monad.
            set=set_vars,
            var=set_vars,

            # === EXECUTION MODES ===
            dry_run=request.dry_run,
            force=request.force,

            # === THE VOICE OF THE SCRIBE ===
            # We map the integer `verbosity` back to boolean flags.
            verbose=(request.verbosity > 0),
            silent=(request.verbosity < 0),

            # === GNOSTIC INSPECTION ===
            preview=request.preview,
            audit=request.audit,
            lint=request.lint,

            # === INTERACTION GOVERNANCE ===
            non_interactive=request.non_interactive,

            # === SPECIFIC ARTIFACTS ===
            arch_path=request.arch_path,
            log=request.log_file,

            # === THE MAESTRO'S WILL ===
            # New flag to suppress post-run commands (e.g. for security or speed).
            no_edicts=request.no_edicts,

            # === DEFAULTS FOR MISSING ATTRIBUTES ===
            # The SymphonyConductor expects these attributes to exist, even if None.
            # Providing them prevents `AttributeError` heresies in the legacy code.
            task=None,  # We run the whole symphony, not a specific task
            rehearse=False,  # Arch implies a manifest reality, not a rehearsal
            manifest=True,  # We are manifesting, not just checking
            no_cleanup=False,  # Standard cleanup rules apply

            # Future-proofing: Catch-all for any other attributes the engines might probe
            # that are not explicitly in the Request model.
            **request.model_extra if request.model_extra else {}
        )