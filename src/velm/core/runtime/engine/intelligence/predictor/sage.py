# Path: src/velm/core/runtime/engine/intelligence/predictor/sage.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: DETERMINISTIC_SAGE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SAGE_V420_CAUSAL_GRIMOIRE
# =========================================================================================

from typing import Dict, List, Any, Optional, Set, Final, Iterable
from collections import defaultdict
from .contracts import HeresyState


# =========================================================================================
# == THE GNOSTIC SAGE                                                                    ==
# =========================================================================================

class GnosticSage:
    """
    =======================================================================================
    == THE GNOSTIC SAGE (V-Ω-TOTALITY)                                                   ==
    =======================================================================================
    LIF: ∞ | ROLE: CAUSAL_ADJUDICATOR | RANK: MASTER

    The hardcoded wisdom of the Predictor. It provides the "Reason" that balances
     the "Probability" of the Markov mind.
    """

    # [ASCENSION 4]: THE SACRED BEGINNINGS (BOOTSTRAP PHASE)
    SACRED_BEGINNINGS: Final[List[str]] = [
        "InitRequest",
        "ManifestRequest",
        "AnalyzeRequest",
        "ArchetypeRequest"
    ]

    # [ASCENSION 3]: SEMANTIC GRAVITY WELLS (INTENT CLUSTERS)
    # Rites in the same cluster increase each other's weight.
    INTENT_CLUSTERS: Final[Dict[str, Set[str]]] = {
        "CREATION": {"GenesisRequest", "CreateRequest", "ManifestRequest", "WeaveRequest"},
        "ADJUDICATION": {"AnalyzeRequest", "LintRequest", "VerifyRequest", "AuditRequest", "MRIRequest"},
        "TRANSMUTATION": {"RefactorRequest", "TransmuteRequest", "PatchRequest", "BeautifyRequest"},
        "CHRONOLOGY": {"HistoryRequest", "UndoRequest", "BlameRequest", "ReplayRequest"},
        "COMMUNION": {"ScribeRequest", "SummarizeRequest", "TranslateRequest", "ChatRequest"}
    }

    # [ASCENSION 2]: THE REDEMPTIVE CHAINS (FRACTURE RECOVERY)
    # Targeted response to specific failure states.
    REDEMPTION_LATTICE: Final[Dict[str, List[str]]] = {
        "CRITICAL": ["RepairRequest", "UndoRequest", "AnalyzeRequest"],
        "WARNING": ["AnalyzeRequest", "LintRequest", "RefactorRequest"],
        "SECURITY": ["AuditRequest", "SecretRequest", "VeilRequest"]
    }

    # [ASCENSION 1]: STRATUM-SPECIFIC WISDOM
    # The Sage knows that different languages require different rhythms.
    STRATUM_WISDOM: Final[Dict[str, List[str]]] = {
        "python": ["RunRequest", "TestRequest", "FormatRequest"],
        "typescript": ["BuildRequest", "TestRequest", "LintRequest"],
        "rust": ["BuildRequest", "VerifyRequest", "BenchRequest"],
        "container": ["VesselRequest", "DeployRequest", "StatusRequest"]
    }

    def advise(self,
               last_rite: Optional[str],
               state: HeresyState,
               history: List[str],
               metadata: Dict[str, Any]) -> Dict[str, float]:
        """
        ===================================================================================
        == THE RITE OF DETERMINISTIC COUNSEL (ADVISE)                                    ==
        ===================================================================================
        Divines the most logical path based on the Grimoire of Causal Laws.
        """
        advice_matrix: Dict[str, float] = defaultdict(float)
        history_len = len(history)

        # --- MOVEMENT I: THE VOID HANDLING ---
        if history_len == 0 or not last_rite:
            return {r: 0.95 for r in self.SACRED_BEGINNINGS}

        # --- MOVEMENT II: THE REDEMPTION GATE ---
        if state == HeresyState.FRACTURED:
            # [ASCENSION 2]: Priority 1 is healing.
            # Redirect all metabolic energy to the Redemption Lattice.
            for i, rite in enumerate(self.REDEMPTION_LATTICE["CRITICAL"]):
                advice_matrix[rite] += 1.5 / (i + 1)
            return advice_matrix

        # --- MOVEMENT III: CAUSAL SUCCESSION ---
        # If the last action was Creation, suggest Adjudication or Transmutation.
        last_cluster = self._divine_cluster(last_rite)

        if last_cluster == "CREATION":
            self._apply_weight(advice_matrix, self.INTENT_CLUSTERS["ADJUDICATION"], 0.8)
            self._apply_weight(advice_matrix, ["RunRequest"], 0.6)

        elif last_cluster == "ADJUDICATION":
            # After analysis, usually comes Transmutation (Fixing) or Chronology (Saving)
            self._apply_weight(advice_matrix, self.INTENT_CLUSTERS["TRANSMUTATION"], 0.7)
            self._apply_weight(advice_matrix, ["SaveRequest", "HistoryRequest"], 0.5)

        elif last_cluster == "TRANSMUTATION":
            # After fixing, must re-verify.
            self._apply_weight(advice_matrix, ["VerifyRequest", "AnalyzeRequest"], 0.9)

        # --- MOVEMENT IV: STRATUM ALIGNMENT ---
        # [ASCENSION 1]: Inject language-specific best practices.
        project_type = metadata.get("project_type", "python").lower()
        if project_type in self.STRATUM_WISDOM:
            self._apply_weight(advice_matrix, self.STRATUM_WISDOM[project_type], 0.4)

        # --- MOVEMENT V: PERSONA BIAS ---
        # [ASCENSION 5]: Favor specific rites based on the Architect's current Mask.
        persona = metadata.get("persona", "architect").lower()
        if "security" in persona:
            self._apply_weight(advice_matrix, self.INTENT_CLUSTERS["ADJUDICATION"], 0.5)
        elif "scribe" in persona:
            self._apply_weight(advice_matrix, self.INTENT_CLUSTERS["COMMUNION"], 0.5)

        # --- MOVEMENT VI: RECURSION GUARD ---
        # [ASCENSION 11]: Never suggest the same rite twice in a row deterministically.
        if last_rite in advice_matrix:
            advice_matrix[last_rite] *= 0.1

        return dict(advice_matrix)

    def _divine_cluster(self, rite_name: str) -> Optional[str]:
        """Perceives which gravity well a rite belongs to."""
        for cluster, rites in self.INTENT_CLUSTERS.items():
            if rite_name in rites:
                return cluster
        return None

    def _apply_weight(self, matrix: Dict[str, float], rites: Iterable[str], weight: float):
        """Inscribes weight into the advice matrix."""
        for rite in rites:
            matrix[rite] += weight

    def get_rationale(self, suggestion: str, last_rite: str) -> str:
        """
        [ASCENSION 11]: SOCRATIC RATIONALE.
        Provides the architectural reasoning for a specific suggestion.
        """
        cluster = self._divine_cluster(suggestion)

        if suggestion == "RepairRequest":
            return "The previous rite fractured; initiating automated redemption."
        if cluster == "ADJUDICATION":
            return f"Analyzing the recently manifest form of {last_rite} for structural heresies."
        if cluster == "TRANSMUTATION":
            return f"Purifying the logic of {last_rite} to achieve titanium stability."
        if cluster == "COMMUNION":
            return "Chronicling the current state of Gnosis for future Architects."

        return "Following the optimal path of architectural evolution."

# == SCRIPTURE SEALED: THE SAGE HAS SPOKEN ==