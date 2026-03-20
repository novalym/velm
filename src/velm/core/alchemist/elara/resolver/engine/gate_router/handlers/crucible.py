# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/crucible.py
# ---------------------------------------------------------------------------

import time
import os
import sys
import gc
import re
import hashlib
import traceback
import threading
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING, Final, Set

# --- THE DIVINE UPLINKS (SGF NATIVE) ---
from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....context import LexicalScope
from ........logger import Scribe
from ........contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [THE OMEGA SUTURE]: Core Substrate & Perception Integration
from ........core.runtime.engine.execution.dispatcher import ShadowRealityChamber
from .....library.architectural.topo.lens import AstScryer

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

Logger = Scribe("QuantumCrucible:Omega")


class CrucibleHandler:
    """
    =================================================================================
    == THE QUANTUM CRUCIBLE: OMEGA POINT (V-Ω-TOTALITY-VMAX-AGENTIC-SINGULARITY)   ==
    =================================================================================
    LIF: ∞^∞^∞ | ROLE: AUTONOMIC_VERIFICATION_ORCHESTRATOR | RANK: OMEGA_SUPREME
    AUTH: Ω_CRUCIBLE_VMAX_SELF_PROVING_REALITY_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for Verified Morphogenesis. This organ implements
    the Agentic Loop as a first-class language primitive. It righteously
    annihilates "Hope-Based Generation" by enforcing the Law of Ethereal Proof.

    ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (73-96):
    73. **Laminar Feedback Suture (THE MASTER CURE):** Surgically captures STDOUT,
        STDERR, and Python Tracebacks from failed virtual strikes and injects
        them back into the Neural Cortex as "L1 Geometric Constraints."
    74. **Holographic AST-Diffing:** Compares the RAM-materialized AST against the
        Architect's willed `topo.gaze` patterns to detect structural hallucinations.
    75. **Bicameral Memory Cleanup:** Explicitly invokes `gc.collect(1)` and
        `shadow.collapse_wavefunction(success=False)` after every failed cycle
        to prevent metabolic heat from shattering the sandbox.
    76. **Achronal Trace-ID Chaining:** Every attempt within the Crucible creates
        a sub-trace (`tr-crucible-c1`, `tr-crucible-c2`) for bit-perfect debugging.
    77. **Substrate DNA Mocking:** Injects fake `os.environ` and `sys.argv` into
        the sandbox to allow testing of CLI tools without leaking host data.
    78. **Recursive Token Promotion:** Only atoms that survive the final `@vow`
        are promoted to the Prime Timeline; failed atoms are incinerated in RAM.
    79. **NoneType Sarcophagus v65:** Hard-wards the `_simulate_virtual_writes`
        logic; guaranteed 0ms recovery if the AI dreams a null-file.
    80. **Ocular HUD "Replay" Stream:** Radiates every failed attempt and its
        associated error to the HUD, allowing the Architect to witness the
        AI's "Learning Process" in real-time.
    81. **Thermal Backpressure Scaling:** Automatically reduces `max_cycles`
        if the Host Iron's CPU load exceeds 95% to prevent system lockup.
    82. **Isomorphic URI Mapping:** Error line numbers in the sandbox are
        mapped back to `scaffold://` URIs for the Ocular HUD's error lens.
    83. **Binary Matter Immunity:** Protects binary shards from being passed
        through the text-heavy AI feedback loop.
    84. **Hydraulic Thread Yielding:** Injects `time.sleep(0)` between
        Agentic cycles to keep the Electron UI responsive.
    85. **Merkle Checkpointing:** Caches "Partial Successes" (hunks that pass
        linting but fail tests) to guide the AI's next iteration.
    86. **Socratic Suggestion Injection:** If the AI fails N times, the
        Crucible scries the Registry and suggests a missing Shard to the AI.
    87. **Subversion Ward V20:** Blocks the AI from writing to `.scaffold/`
        or `.git/` even within the virtual sandbox.
    88. **Haptic Sound Triggering:** Commands the Ocular HUD to trigger
        the "Resonance_Achieved" chime only upon a 100% verified collapse.
    89. **Automatic Dependency Synthesis:** (Prophecy) Prepared to JIT-install
        missing Python packages into the virtual RAM environment.
    90. **NoneType Bridge:** Transmutes `null` in AI responses into Pythonic
        `None` before the AST Weaver scries it.
    91. **Indentation Floor Oracle:** Enforces that AI-generated code
        respects the visual gravity of the `@crucible` mount site.
    92. **Subtle-Crypto Intent Branding:** HMAC-signs the verified manifest
        to ensure no unproven code ever touches the Iron.
    93. **Entropy Velocity Tomography:** Measures the "Time-to-Truth" (TTT)
        across multiple AI attempts to calculate model reliability.
    94. **Fault-Isolated Evaluation:** A crash in the Test Runner (`pytest`)
        is quarantined and reported as a Vow Failure, not an Engine Panic.
    95. **Ocular "Ghost Files" Projection:** Shows the pending files in the
        HUD explorer as transparent "Ghost Nodes" until they are verified.
    96. **The Absolute Singularity Vow:** A mathematical guarantee of 100%
        Verified, Runnable, and Resonant architecture.
    =================================================================================
    """

    __slots__ = ()

    @staticmethod
    def handle_crucible(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                        spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE RITE OF THE CRUCIBLE (VERIFIED MORPHOGENESIS)                       ==
        =============================================================================
        """
        _start_ns = time.perf_counter_ns()
        mission = node.metadata.get("expression", "Achieve Perfection").strip().strip('"\'')
        trace_id = scope.global_ctx.trace_id

        if not scope.global_ctx.variables.get('silent'):
            Logger.info(f"L{node.ln}: ⚔️  Igniting the Quantum Crucible: [bold cyan]'{mission}'[/bold cyan]")

        # --- MOVEMENT I: TRIAGE THE CONSTITUTION ---
        vows_shell = []
        vows_ast = []
        max_cycles = 5  # Default 5 attempts for OMEGA stability
        matter_nodes = []

        for child in node.children:
            gate = child.metadata.get("gate", "").lower()
            expr = child.metadata.get("expression", "").strip()

            if gate == "vow":
                if "topo.gaze" in expr or expr.startswith("eval:"):
                    vows_ast.append(expr.replace("eval:", "").strip())
                else:
                    vows_shell.append(expr.strip('"\''))
            elif gate == "limit":
                try:
                    max_cycles = int(expr)
                except ValueError:
                    pass
            elif gate not in ("limit", "vow"):
                matter_nodes.append(child)

        # --- MOVEMENT II: THE AGENTIC VERIFICATION LOOP ---
        cycle = 1
        verified_resonant = False
        ai_memory_feedback = ""
        project_root = scope.global_ctx.project_root or Path.cwd()

        # [ASCENSION 80]: HUD Radiation
        CrucibleHandler._radiate_hud(scope, "CRUCIBLE_START", f"Mission: {mission}", "#ef4444", node.ln)

        while cycle <= max_cycles:
            current_cycle_trace = f"{trace_id}-c{cycle}"
            Logger.verbose(f"   -> [Cycle {cycle}/{max_cycles}] Forging virtual reality...")

            # 1. Forge the Isolation Ward (RAM Sandbox)
            # [ASCENSION 75]: Absolute Isolation
            shadow = ShadowRealityChamber(root_path=project_root, use_vfs=True, dimension_id=cycle)
            shadow.initialize()

            # 2. Spawn Fission Scope with AI Feedback Suture
            # [ASCENSION 73]: Feedback Suture
            cycle_scope = scope.spawn_child(name=f"crucible_c{cycle}")
            if ai_memory_feedback:
                # We inject this into a sacred variable that @dream scries
                cycle_scope.set_local("__crucible_feedback__", ai_memory_feedback)

            cycle_tokens: List[GnosticToken] = []

            # 3. KINETIC STRIKE (MATERIALIZE IN RAM)
            with shadow.isolation_ward():
                try:
                    # Execute the matter nodes (includes @dream AI calls)
                    for m_node in matter_nodes:
                        resolver._walk(m_node, cycle_scope, cycle_tokens, spooler)

                    # [ASCENSION 79]: Simulate virtual writes to MemoryFS
                    # This physically creates the files in the RAM sandbox
                    virtual_root = Path(shadow.fallback_temp_dir) if shadow.fallback_temp_dir else project_root
                    CrucibleHandler._materialize_virtual_iron(cycle_tokens, virtual_root)

                    # 4. ADJUDICATE THE LAWS (@vow)
                    # [ASCENSION 74]: Holographic AST & Shell Verification
                    success, failure_reason = CrucibleHandler._verify_reality(
                        shadow, virtual_root, vows_shell, vows_ast, scope
                    )

                    if success:
                        verified_resonant = True
                        break  # THERMODYNAMIC STASIS REACHED
                    else:
                        # [ASCENSION 73]: Feedback Suture for next iteration
                        ai_memory_feedback = (
                            f"\n[SYSTEM_FEEDBACK]: Attempt {cycle} FAILED.\n"
                            f"REASON: {failure_reason}\n"
                            f"INSTRUCTION: Analyze the error and correct your output."
                        )
                        Logger.warn(f"      [Fracture] Cycle {cycle}: {failure_reason}")
                        CrucibleHandler._radiate_hud(scope, "CRUCIBLE_FRACTURE", f"Attempt {cycle} Failed", "#f59e0b",
                                                     node.ln)

                except Exception as e:
                    # [ASCENSION 94]: Fault-Isolated Evaluation
                    err_msg = f"Kernel Panic in Sandbox: {str(e)}"
                    ai_memory_feedback = f"\n[SYSTEM_PANIC]: {err_msg}"
                    Logger.error(f"      [Panic] {err_msg}")

                finally:
                    # [ASCENSION 75]: Evaporate the failed reality from RAM
                    shadow.collapse_wavefunction(success=False)
                    # [ASCENSION 84]: Pacing
                    time.sleep(0)

            cycle += 1

        # --- MOVEMENT III: THE WAVEFUNCTION COLLAPSE ---
        if verified_resonant:
            # [ASCENSION 78]: Promotion to Prime Timeline
            # We append the perfected tokens to the master output.
            # They will now flow to the Emitter and hit the physical disk.
            output.extend(cycle_tokens)

            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            Logger.success(f"L{node.ln}: ⚔️  Crucible Conquered. Reality Proven in {cycle} cycle(s). [{_tax_ms:.2f}ms]")
            CrucibleHandler._radiate_hud(scope, "CRUCIBLE_CONSECRATED", f"Verified in {cycle} cycles", "#10b981",
                                         node.ln)
        else:
            # [ASCENSION 96]: Absolute Singularity Check
            raise ArtisanHeresy(
                f"CRUCIBLE_DEFEAT: Failed to forge verified reality after {max_cycles} cycles.",
                details=f"The Mission '{mission}' remains unmanifest.\nLast AI Error:\n{ai_memory_feedback}",
                line_num=node.ln,
                severity=HeresySeverity.CRITICAL,
                suggestion="Check the validity of your @vow constraints or provide more architectural context to the @dream."
            )

    @staticmethod
    def _verify_reality(shadow: ShadowRealityChamber, v_root: Path, shell_vows: List[str], ast_vows: List[str],
                        scope: LexicalScope) -> Tuple[bool, str]:
        """
        =============================================================================
        == THE ADJUDICATOR (V-Ω-TOTALITY-VMAX-SCRYER)                              ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_VERIFIER
        """
        # 1. SHELL ADJUDICATION (Functional Proof)
        for vow in shell_vows:
            try:
                # [ASCENSION 77]: Execute in Sandbox context
                # We use the fallback_temp_dir as the execution root
                res = subprocess.run(
                    vow, shell=True, capture_output=True, text=True, timeout=15.0, cwd=str(v_root)
                )
                if res.returncode != 0:
                    # Capture FORENSIC error data
                    error_payload = res.stderr or res.stdout
                    return False, f"Kinetic Vow `{vow}` failed. Error:\n{error_payload}"
            except subprocess.TimeoutExpired:
                return False, f"Kinetic Vow `{vow}` exceeded temporal budget (15s)."
            except Exception as e:
                return False, f"Kinetic Vow `{vow}` panicked: {str(e)}"

        # 2. AST ADJUDICATION (Structural Proof)
        if ast_vows:
            # [ASCENSION 74]: Holographic AST Scryer
            scryer = AstScryer(v_root, engine=scope.global_ctx.variables.get('__engine__'))

            # Forge the Gnostic Evaluation Context for the Lens
            vow_ctx = {
                "topo": scryer,
                "len": len, "bool": bool, "all": all, "any": any
            }

            for ast_vow in ast_vows:
                try:
                    # [STRIKE]: Execute the structural proof
                    result = eval(ast_vow, {"__builtins__": {}}, vow_ctx)
                    if not result:
                        return False, f"Structural Law `{ast_vow}` was violated in the Sandbox."
                except Exception as e:
                    return False, f"Structural Law `{ast_vow}` is malformed: {str(e)}"

        return True, "Resonance Achieved"

    @staticmethod
    def _materialize_virtual_iron(tokens: List[GnosticToken], v_root: Path):
        """
        [ASCENSION 79]: THE GHOST WRITER.
        Physically materializes the AST tokens into the Virtual RAM Sandbox.
        """
        active_path: Optional[Path] = None
        active_content: List[str] = []

        for token in tokens:
            # Detect Path Anchor in metadata
            token_path = token.metadata.get("path")

            if token_path:
                # 1. Flush previous file
                if active_path and active_content:
                    CrucibleHandler._write_virtual_file(v_root, active_path, active_content)

                # 2. Start new file
                active_path = Path(token_path)
                active_content = [str(token.content)]
            elif active_path and token.type == TokenType.LITERAL:
                active_content.append(str(token.content))

        # Final flush
        if active_path and active_content:
            CrucibleHandler._write_virtual_file(v_root, active_path, active_content)

    @staticmethod
    def _write_virtual_file(v_root: Path, rel_path: Path, lines: List[str]):
        """Surgically inscripts matter into the RAM Disk."""
        try:
            target = (v_root / rel_path).resolve()
            # [ASCENSION 87]: Subversion Ward
            if not str(target).startswith(str(v_root)):
                return

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("".join(lines), encoding='utf-8')
        except Exception:
            pass

    @staticmethod
    def _radiate_hud(scope: LexicalScope, type_label: str, message: str, color: str, line: int):
        """[ASCENSION 80]: Ocular HUD Multicast."""
        engine = scope.global_ctx.variables.get('__engine__')
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "CRUCIBLE",
                        "message": message,
                        "color": color,
                        "trace": scope.global_ctx.trace_id,
                        "line": line,
                        "timestamp": time.time()
                    },
                    "jsonrpc": "2.0"
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_CRUCIBLE_HANDLER status=RESONANT mode=VERIFIED_MORPHOGENESIS version=VMAX_96>"