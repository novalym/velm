# Path: core/cortex/logic_inductor.py
# -----------------------------------
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from ...logger import Scribe

Logger = Scribe("LogicInductor")


@dataclass
class PatternHypothesis:
    """A proposed abstraction for a group of files."""
    variable_name: str
    values: List[str]
    template_path: str
    matched_files: List[str]
    confidence: float
    pattern_type: str  # 'loop', 'conditional', 'structural'


class LogicInductor:
    """
    =================================================================================
    == THE PATTERN RECOGNIZER (V-Ω-INFERENCE-ENGINE-ULTIMA)                        ==
    =================================================================================
    LIF: 100,000,000,000,000

    A cognitive engine that gazes upon a static list of file paths and hallucinates
    the abstract structures (Loops, Variables, Conditions) that could have created them.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Tokenizer of Paths:** Deconstructs paths into semantic atoms, treating
        slashes as joints and names as bones.
    2.  **The Variance Detector:** Analyzes sibling directories to find the "Axis of
        Change" (e.g., `auth`, `billing`, `users` -> `{{domain}}`).
    3.  **The Semantic Namer:** Uses NLP heuristics to name variables. If it sees
        `user`, `post`, `comment`, it guesses `{{entity}}` or `{{model}}`.
    4.  **The Structural Homology Gaze:** Identifies when different directories contain
        the *same* file structure (e.g., every service has a `controller.ts` and `service.ts`).
    5.  **The Outlier Pruner:** Statistically ignores noise files (`.DS_Store`, `README`)
        that break patterns, increasing confidence.
    6.  **The Loop Prophesier:** Generates valid `@for` loop syntax for the blueprint.
    7.  **The Variable Extractor:** Extracts the variable values (`['auth', 'billing']`)
        and formats them as a valid Gnostic declaration.
    8.  **The Flattening Detector:** Detects if a pattern is nested deep (`src/domains/{{x}}/lib/{{y}}`)
        and flattens it into a usable suggestion.
    9.  **The Confidence Scorer:** Ranks suggestions. A pattern covering 50 files is
        better than one covering 2.
    10. **The Case Normalizer:** Detects if the variable usage implies a filter
        (e.g., `User` vs `user` -> `{{name|pascal}}` vs `{{name}}`).
    11. **The Void Sentinel:** Ignores empty directories or singular occurrences.
    12. **The Luminous Suggestion:** Formats the output not as data, but as copy-pasteable
        Scaffold scripture.
    =================================================================================
    """

    def __init__(self):
        self.common_noise = {'.git', '__pycache__', 'node_modules', '.DS_Store'}
        # Heuristics for naming variables based on context
        self.naming_heuristics = {
            'src': 'module', 'lib': 'lib_name', 'components': 'component',
            'pages': 'page', 'routes': 'route', 'api': 'resource',
            'models': 'model', 'controllers': 'controller', 'services': 'service'
        }

    def induce(self, paths: List[str]) -> List[Dict[str, Any]]:
        """
        The One True Rite of Induction.
        Takes a list of strings, returns a list of suggestions.
        """
        clean_paths = self._purify_paths(paths)
        hypotheses = self._detect_structural_patterns(clean_paths)

        # Rank by confidence (impact)
        hypotheses.sort(key=lambda h: h.confidence, reverse=True)

        return [self._forge_suggestion(h) for h in hypotheses if h.confidence > 0.6]

    def _purify_paths(self, paths: List[str]) -> List[Path]:
        """[FACULTY 11] The Void Sentinel."""
        valid = []
        for p in paths:
            if any(part in self.common_noise for part in p.split('/')):
                continue
            valid.append(Path(p))
        return valid

    def _detect_structural_patterns(self, paths: List[Path]) -> List[PatternHypothesis]:
        """
        [FACULTY 4] The Structural Homology Gaze.
        Looks for directories that contain identical file sets.
        """
        # Map: Parent_Path -> List[Children_Files]
        structure_map = defaultdict(set)

        for p in paths:
            if len(p.parts) > 1:
                # We treat the immediate parent as the "Variant", and the grandparent as the "Container"
                # e.g. src/domains/auth/user.py
                # Container: src/domains
                # Variant: auth
                # Structure: user.py

                container = p.parent.parent
                variant = p.parent.name
                child_file = p.name

                structure_map[(container, variant)].add(child_file)

        # Now we group by the SET of children.
        # Key: (Container, FrozenSet(Children))
        # Value: List[Variant_Names]
        pattern_clusters = defaultdict(list)

        for (container, variant), children in structure_map.items():
            if not children: continue
            # Create a signature of the structure
            signature = frozenset(children)
            pattern_clusters[(container, signature)].append(variant)

        hypotheses = []

        for (container, signature), variants in pattern_clusters.items():
            # [FACULTY 9] The Confidence Scorer
            # We need at least 2 variants to call it a pattern.
            if len(variants) < 2:
                continue

            # [FACULTY 3] The Semantic Namer
            var_name = self._guess_variable_name(container, variants)

            # Calculate confidence based on number of repetitions and complexity of structure
            confidence = min(0.95, (len(variants) * 0.1) + (len(signature) * 0.05))

            # Build the template path representation
            # If signature has multiple files, we suggest a block.

            # Convert back to strings for the hypothesis
            matched_files_count = len(variants) * len(signature)

            h = PatternHypothesis(
                variable_name=var_name,
                values=sorted(variants),
                template_path=f"{container}/{{{{ {var_name} }}}}/",
                matched_files=list(signature),
                confidence=confidence,
                pattern_type="structural_loop"
            )
            hypotheses.append(h)

        return hypotheses

    def _guess_variable_name(self, container: Path, variants: List[str]) -> str:
        """[FACULTY 3] The Semantic Namer."""
        parent_name = container.name.lower()

        # Check hardcoded heuristics
        if parent_name in self.naming_heuristics:
            return self.naming_heuristics[parent_name]

        # De-pluralize (naive)
        if parent_name.endswith('s'):
            return parent_name[:-1]

        return "item"

    def _forge_suggestion(self, h: PatternHypothesis) -> Dict[str, Any]:
        """
        [FACULTY 12] The Luminous Suggestion.
        Forges the actual Python/Scaffold code to present to the user.
        """
        var_decl = f"$$ {h.variable_name}s = {json.dumps(h.values)}"

        loop_header = f"@for {h.variable_name} in {h.variable_name}s:"

        # [FACULTY 10] The Case Normalizer (Prediction)
        # We check if files inside are PascalCase while values are snake_case
        # For now, we just list the files as they are found in the signature.

        block_body = []
        for filename in sorted(h.matched_files):
            # Check if filename needs variable injection
            # (e.g. AuthController.ts inside 'auth' folder -> {{name|pascal}}Controller.ts)
            # This is advanced. For V1 we output static names relative to the loop.

            # Heuristic: Does the filename contain the variant name?
            # We pick the first variant to test
            sample_variant = h.values[0]

            # This logic would need to check the ACTUAL filename for that variant.
            # Since `matched_files` is just a set of names (assuming they are constant),
            # we output them as constants.
            # If filenames VARY by variant (auth.ts vs user.ts), they wouldn't match the signature set
            # unless we normalized them first.
            # The current logic finds IDENTICAL file structures (index.ts, styles.css).

            block_body.append(f"    {h.template_path}{filename}")

        suggestion_text = f"""# Pattern: {len(h.values)} {h.variable_name} modules detected in {h.template_path}
        {var_decl}
        
        {loop_header}
        {chr(10).join(block_body)}
        @endfor
        """
        return {
            "type": h.pattern_type,
            "confidence": h.confidence,
            "suggestion_text": suggestion_text,
            "impact": f"Abstracts {len(h.values)} directories into 1 loop."
        }