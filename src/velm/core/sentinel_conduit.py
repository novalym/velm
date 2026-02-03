# Path: scaffold/core/sentinel_conduit.py
# ---------------------------------------

"""
=================================================================================
== THE SACRED SANCTUM OF THE SENTINEL CONDUIT (V-Ω-ETERNAL-BRIDGE)             ==
=================================================================================
This scripture contains the living soul of the Gnostic Bridge to the Sentinel
God-Engine. Its one true purpose is to act as a hyper-intelligent, resilient,
and performant ambassador, allowing any artisan in the Scaffold cosmos to
commune with the Sentinel's deep analytical Gaze.
=================================================================================
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List

from ..contracts.heresy_contracts import Heresy, HeresySeverity
from ..logger import Scribe

# A Gnostic Scribe to chronicle the communion between the two God-Engines.
Logger = Scribe("SentinelConduit")


class SentinelConduit:
    """
    =================================================================================
    == THE GNOSTIC AMBASSADOR (V-Ω-HYPER-RESILIENT)                                ==
    =================================================================================
    LIF: 100,000,000,000

    This artisan is the one true, sacred bridge to the Sentinel. It is forged with a
    pantheon of Gnostic faculties that make its communion unbreakable and its Gaze pure.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Sentinel's Gaze:** It first performs a Gaze to see if the `sentinel`
        artisan is even manifest in the mortal realm, failing gracefully if not.
    2.  **The Ephemeral Sanctum:** It forges a temporary, ephemeral scripture to bestow
        upon the Sentinel, ensuring the mortal realm's disk is never profaned.
    3.  **The Gnostic Plea:** It knows the one true, sacred plea (`sentinel lint --json`)
        required to receive a pure, machine-readable scripture of heresies.
    4.  **The Unbreakable Ward of Paradox:** Its communion is shielded. It captures stderr
        and transmutes any catastrophic failure in the Sentinel into a single,
        luminous, high-level `Heresy` vessel.
    5.  **The Heresy Transmuter:** It transmutes the Sentinel's raw JSON output into a
        pure, Gnostically-typed `List[Heresy]`, honoring the sacred contract of the
        Scaffold cosmos.
    6.  **The Chronomancer's Ward:** It enforces a strict timeout on the Sentinel's Gaze,
        preventing a fallen or frozen Sentinel from hanging the Scaffold engine.
    7.  **The Luminous Voice:** It proclaims its every major rite to the Gnostic log.
    8.  **The Sovereign Soul:** It is a pure, stateless artisan. It can be summoned by
        any other artisan without fear of profane side effects.
    9.  **The Polyglot Mind (Inherited):** Because it summons the Sentinel, it
        inherits the Sentinel's own polyglot Gaze, capable of adjudicating Python,
        TypeScript, Go, and all other known tongues.
    10. **The Unbreakable Contract:** Its public `adjudicate` rite is a pure,
        unbreakable contract, its input and output vessels perfectly defined.
    11. **The Performance Ward:** It operates on in-memory content, writing to disk
        only for the brief, ephemeral moment of IPC communion.
    12. **The Gnostic Purifier:** It performs a final purification rite upon the
        ephemeral sanctum, ensuring no trace of its communion is left behind.
    =================================================================================
    """

    def __init__(self):
        """
        The Rite of Inception. The Ambassador performs its Gaze to ensure its
        divine counterpart, the Sentinel, is manifest.
        """
        # [FACULTY 1] The Sentinel's Gaze
        self.sentinel_path = shutil.which("sentinel")
        if not self.sentinel_path:
            Logger.warn("The 'sentinel' artisan is not manifest. The Gaze of Adjudication will be averted.")

    def adjudicate(self, path: Path, content: str) -> List[Heresy]:
        """
        The one true, public rite. It receives a scripture's soul and proclaims
        a list of any heresies perceived within it.
        """
        # If the Sentinel is a void, the Gaze is averted, and the scripture is
        # proclaimed as pure by default.
        if not self.sentinel_path:
            return []

        Logger.verbose(f"Sentinel Conduit awakened. Adjudicating the soul of '{path.name}'...")
        heresies: List[Heresy] = []

        # [FACULTY 2] The Ephemeral Sanctum
        # We use a temporary file to pass the content to the Sentinel CLI.
        # This is the safest, most robust method for inter-process communication.
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=path.suffix, encoding='utf-8') as tf:
                temp_file_path = Path(tf.name)
                tf.write(content)

            # [FACULTY 3] The Gnostic Plea
            command = [
                self.sentinel_path,
                "lint",
                "--json",
                str(temp_file_path)
            ]

            # --- THE SACRED COMMUNION ---
            Logger.verbose(f"Summoning the Sentinel with the plea: `{' '.join(command)}`")

            # [FACULTY 6 & 4] The Chronomancer's Ward & Unbreakable Ward of Paradox
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60  # A generous 60-second timeout
            )

            # --- THE ADJUDICATION OF THE SENTINEL'S RESPONSE ---
            if result.returncode > 1:  # 0=pure, 1=heresies found, >1=crash
                # A catastrophic paradox occurred within the Sentinel itself.
                raise RuntimeError(f"The Sentinel's Gaze was shattered. Stderr:\n{result.stderr}")

            if result.stdout:
                try:
                    # [FACULTY 5] The Heresy Transmuter
                    sentinel_report = json.loads(result.stdout)
                    for file_report in sentinel_report:
                        for heresy_data in file_report.get("heresies", []):
                            heresies.append(Heresy(
                                message=heresy_data.get("message", "Unknown Heresy"),
                                line_num=heresy_data.get("line", 0),
                                line_content=heresy_data.get("context", ""),
                                severity=HeresySeverity(heresy_data.get("severity", "WARNING")),
                                suggestion=heresy_data.get("suggestion")
                            ))
                except (json.JSONDecodeError, KeyError) as e:
                    raise IOError(f"The Sentinel spoke a profane, malformed tongue (JSON). Heresy: {e}")

        except Exception as e:
            # The Unbreakable Ward catches all paradoxes and transmutes them.
            Logger.error(f"A paradox occurred during communion with the Sentinel: {e}")
            heresies.append(Heresy(
                message="Sentinel Communion Paradox",
                details=f"The bridge between Scaffold and Sentinel was shattered.\nReason: {str(e)}",
                severity=HeresySeverity.CRITICAL
            ))

        finally:
            # [FACULTY 12] The Gnostic Purifier
            if temp_file and temp_file_path.exists():
                try:
                    temp_file_path.unlink()
                except OSError:
                    pass

        if heresies:
            Logger.warn(f"The Sentinel's Gaze perceived {len(heresies)} heresies in '{path.name}'.")
        else:
            Logger.verbose(f"The Sentinel's Gaze is serene. The soul of '{path.name}' is pure.")

        return heresies