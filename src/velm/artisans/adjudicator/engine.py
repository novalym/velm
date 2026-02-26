# Path: artisans/adjudicator/engine.py
# --------------------------------------
import time
from pathlib import Path
from typing import Dict, List, Any
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import BaseRequest  # Define AdjudicatorRequest in requests.py
from .contracts import AdjudicationReport, ResonanceState
from ...logger import Scribe

Logger = Scribe("LatticeAdjudicator")


class AdjudicatorRequest(BaseRequest):
    target_path: Path
    test_command: str = "make test"
    strict: bool = True


class LatticeAdjudicator(BaseArtisan[AdjudicatorRequest]):
    """
    =================================================================================
    == THE LATTICE ADJUDICATOR (V-Ω-TOTALITY-V25000-RESONANCE-ENGINE)              ==
    =================================================================================
    LIF: ∞ | ROLE: LOGIC_VERIFIER | RANK: OMEGA_SOVEREIGN

    The supreme authority that proves the soul of a project is functional.
    Unlike 'verify' (which checks matter), 'adjudicate' checks LIFE.
    =================================================================================
    """

    def execute(self, request: AdjudicatorRequest) -> ScaffoldResult:
        self._start_ns = time.perf_counter_ns()
        self.logger.info(f"Adjudicator: Initiating Rite of Resonance on [cyan]{request.target_path.name}[/cyan]...")

        # [ASCENSION 1]: SPATIAL ANCHORING
        # We must conduct the test inside the TARGET path (the shadow).
        target = request.target_path.resolve()

        self.progress("Conducting Kinetic Inquest...", 20)

        # [ASCENSION 4]: THE KINETIC STRIKE
        # We use self.io (inherited) to execute the test edict transactionally.
        # But for adjudication, we need the raw output.
        from ...core.maestro import MaestroConductor
        maestro = MaestroConductor(self.engine, self.regs)

        try:
            # We redirect the Maestro's focus to the shadow target
            with self.engine.temporary_context(target):
                self.logger.verbose(f"Maestro Strike: {request.test_command}")
                # [STRIKE]
                vessel = maestro.conduct_raw(request.test_command)

                # Consume the stream
                stdout, stderr = [], []
                while True:
                    try:
                        stream, line = vessel.output_queue.get(timeout=5)
                        if line is None: break
                        if stream == 'stdout':
                            stdout.append(line)
                        else:
                            stderr.append(line)
                    except:
                        break

                vessel.process.wait()
                exit_code = vessel.process.returncode

            # --- MOVEMENT II: THE VERDICT ---
            success = exit_code == 0
            state = ResonanceState.RESONANT if success else ResonanceState.DISHONORANT

            report = AdjudicationReport(
                state=state,
                pass_count=1 if success else 0,  # Future: Parse test numbers
                fail_count=0 if success else 1,
                stdout="\n".join(stdout),
                stderr="\n".join(stderr)
            )

            if not success:
                self.logger.error(f"Logic Fracture detected! Exit Code: {exit_code}")
                if request.strict:
                    return self.failure("Resonance Failed: The shadow reality is logic-fractured.", data=report)

            self.logger.success(f"Resonance Achieved: Shadow is pure and ready for fusion.")
            return self.success("Shadow reality proven resonant.", data=report)

        except Exception as e:
            return self.failure(f"Adjudication Paradox: {e}")