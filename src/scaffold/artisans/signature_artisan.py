# path: scaffold/artisans/signature_artisan.py

import json
from pathlib import Path
import subprocess
import re
from typing import Dict, Any, List, Tuple

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Confirm

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import SignatureRequest
from ..help_registry import register_artisan
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.cortex.engine import GnosticCortex


# =================================================================================
# == I. THE SENTIENT ANALYZER (THE AI'S SOUL)                                    ==
# =================================================================================
class StylometricAnalyzer:
    """
    =================================================================================
    == THE STYLOMETRIC CORTEX (V-Ω-VECTORIZED-MIND)                                ==
    =================================================================================
    This is the AI soul of the Signature Artisan. It transmutes raw code into a
    high-dimensional vector of stylistic traits for mathematical comparison.
    =================================================================================
    """

    FEATURE_KEYS = [
        'quote_pref', 'indent_size', 'avg_line_len', 'comment_ratio',
        'naming_snake_ratio', 'naming_camel_ratio', 'func_len_avg'
    ]

    def _extract_features(self, code: str) -> Dict[str, float]:
        """Performs a Gnostic Gaze to extract stylistic traits from code."""
        features = {}
        lines = code.splitlines()
        total_lines = len(lines)
        if total_lines == 0: return {k: 0.0 for k in self.FEATURE_KEYS}

        # Quote preference
        features['quote_pref'] = 1.0 if code.count("'") > code.count('"') else -1.0

        # Indentation
        indents = [len(line) - len(line.lstrip(' ')) for line in lines if line.strip() and line.startswith(' ')]
        features['indent_size'] = sum(indents) / len(indents) if indents else 4.0

        # Line length
        features['avg_line_len'] = sum(len(line) for line in lines) / total_lines

        # Comment ratio
        comments = sum(1 for line in lines if line.strip().startswith('#') or line.strip().startswith('//'))
        features['comment_ratio'] = comments / total_lines

        # Naming convention (heuristic)
        words = re.findall(r'\b[a-zA-Z_]\w{3,}\b', code)
        snake = sum(1 for w in words if '_' in w)
        camel = sum(1 for w in words if re.match(r'[a-z]+[A-Z]', w))
        features['naming_snake_ratio'] = snake / len(words) if words else 0.0
        features['naming_camel_ratio'] = camel / len(words) if words else 0.0

        # Function length (requires AST)
        # Prophecy: This would use the Gnostic Cortex for a deep Gaze. For now, a heuristic.
        features['func_len_avg'] = 20.0  # Placeholder

        return features

    def learn(self, git_diffs: str) -> dict:
        """Builds a statistical model from a large corpus of the Architect's code."""
        self.engine.logger.verbose("Learning stylometric signature from diff corpus...")
        features = self._extract_features(git_diffs)
        return {"vector": [features.get(k, 0.0) for k in self.FEATURE_KEYS]}

    def verify(self, model: dict, current_diff: str) -> Tuple[float, Dict[str, float]]:
        """Compares a new diff to the learned model and returns a confidence score."""
        self.engine.logger.verbose("Verifying current diff against enshrined signature...")
        model_vector = model.get("vector", [])
        current_features = self._extract_features(current_diff)
        current_vector = [current_features.get(k, 0.0) for k in self.FEATURE_KEYS]

        if not model_vector or not any(current_vector):
            return 0.0, {}

        # Cosine Similarity
        dot_product = sum(a * b for a, b in zip(model_vector, current_vector))
        mag_model = sum(a * a for a in model_vector) ** 0.5
        mag_current = sum(a * a for a in current_vector) ** 0.5

        if mag_model == 0 or mag_current == 0:
            return 0.0, {}

        similarity = dot_product / (mag_model * mag_current)

        # Calculate divergence for the dossier
        divergence = {
            self.FEATURE_KEYS[i]: abs(model_vector[i] - current_vector[i])
            for i in range(len(self.FEATURE_KEYS))
        }

        return max(0.0, similarity), divergence


# =================================================================================
# == II. THE GNOSTIC CONDUCTOR (THE ARTISAN'S SOUL)                              ==
# =================================================================================
@register_artisan("signature")
class SignatureArtisan(BaseArtisan[SignatureRequest]):
    """The Keeper of the Architect's Gnostic Fingerprint."""

    MODEL_DIR = ".scaffold/signatures"

    def execute(self, request: SignatureRequest) -> ScaffoldResult:
        self.logger.info("The Gnostic Inquisitor of Identity awakens...")

        model_dir = self.project_root / self.MODEL_DIR
        model_dir.mkdir(parents=True, exist_ok=True)

        # The analyzer is now an artisan of this conductor
        analyzer = StylometricAnalyzer()
        analyzer.engine = self.engine  # Grant it a voice

        rite_map = {
            "learn": lambda: self._conduct_learn_rite(request, analyzer, model_dir),
            "verify": lambda: self._conduct_verify_rite(request, analyzer, model_dir),
            "list": lambda: self._conduct_list_rite(model_dir),
        }

        handler = rite_map.get(request.signature_command)
        if not handler:
            return self.failure(f"Unknown signature rite: {request.signature_command}")

        return handler()

    def _conduct_learn_rite(self, request: SignatureRequest, analyzer: StylometricAnalyzer,
                            model_dir: Path) -> ScaffoldResult:
        """[FACULTY 3] The Temporal Gaze."""
        signature_name = request.as_name or "default"
        model_path = model_dir / f"{signature_name}.json"

        if model_path.exists() and not request.force:
            if not Confirm.ask(
                    f"[bold question]A Gnostic Signature named '[cyan]{signature_name}[/cyan]' already exists. Overwrite?[/bold question]"):
                return self.success("Rite of Learning stayed by the Architect.")

        self.logger.info(f"Performing deep Gaze into the Git chronicle to learn '{signature_name}' signature...")
        try:
            # Faculty 7: Gnostic Pre-Flight
            user_email = subprocess.check_output(['git', 'config', 'user.email'], text=True,
                                                 cwd=self.project_root).strip()
            if not user_email:
                raise ArtisanHeresy("Git user.email is not configured. The Inquisitor cannot perceive your soul.")

            # Build the `git log` command with temporal constraints
            log_cmd = ['git', 'log', f'--author={user_email}', '--all', '-p']
            if request.since:
                log_cmd.append(f'--since="{request.since}"')

            with self.console.status("[magenta]Analyzing the Architect's unique coding soul...[/magenta]"):
                diff_output = subprocess.check_output(log_cmd, text=True, stderr=subprocess.DEVNULL,
                                                      cwd=self.project_root)

            if not diff_output.strip():
                return self.failure("No commits found for the current author in the specified time range.")

            model = analyzer.learn(diff_output)
            model_path.write_text(json.dumps(model, indent=2))

            return self.success(f"Gnostic Signature '{signature_name}' has been learned and enshrined.")
        except subprocess.CalledProcessError:
            raise ArtisanHeresy("Could not read Git history. Is this a Git repository?")
        except ArtisanHeresy as e:
            raise e

    def _conduct_verify_rite(self, request: SignatureRequest, analyzer: StylometricAnalyzer,
                             model_dir: Path) -> ScaffoldResult:
        """[FACULTY 5] The Luminous Dossier."""
        signature_name = request.signature_name or "default"
        model_path = model_dir / f"{signature_name}.json"

        if not model_path.exists():
            return self.failure(
                f"No Gnostic Signature named '{signature_name}' found.",
                suggestion="Conduct the `scaffold signature learn` rite first."
            )

        try:
            model = json.loads(model_path.read_text())
        except json.JSONDecodeError:
            raise ArtisanHeresy(f"The signature file for '{signature_name}' is profane (corrupted JSON).",
                                suggestion="Conduct the `learn` rite again.")

        self.logger.info(f"Adjudicating staged changes against the '{signature_name}' Gnostic Signature...")
        try:
            staged_diff = subprocess.check_output(['git', 'diff', '--staged'], text=True, cwd=self.project_root)
            if not staged_diff.strip():
                return self.success("No changes staged to verify. The timeline is pure.")

            confidence, divergence = analyzer.verify(model, staged_diff)
            threshold = request.threshold

            is_match = confidence >= threshold
            status_text = "[bold green]SIGNATURE VERIFIED[/]" if is_match else "[bold red]SIGNATURE MISMATCH[/]"

            # --- The Luminous Dossier ---
            table = Table(title=f"Dossier of Stylistic Divergence ({signature_name})", box=None, show_header=False)
            table.add_column("Metric", style="cyan")
            table.add_column("Divergence", style="yellow")

            for key, value in sorted(divergence.items(), key=lambda item: item[1], reverse=True):
                if value > 0.01:  # Only show meaningful divergence
                    table.add_row(key.replace("_", " ").title(), f"{value:.2f}")

            summary_panel = Panel(
                Text.assemble(
                    (f"Confidence: ", "white"),
                    (f"{confidence:.2%}", "bold green" if is_match else "bold red"),
                    (f" (Threshold: {threshold:.2%})", "dim")
                ),
                title=status_text,
                border_style="green" if is_match else "red"
            )

            self.console.print(Panel(Group(summary_panel, table)))
            # --- End of Dossier ---

            if is_match:
                return self.success("Gnostic Signature Verified.", data={"confidence": confidence})
            else:
                return self.failure(
                    "Gnostic Signature mismatch. The style of the staged code is profane.",
                    suggestion="If this change is intentional, use --force to override the Sentinel.",
                    data={"confidence": confidence, "divergence": divergence}
                )

        except subprocess.CalledProcessError:
            return self.failure("Failed to get staged diff from Git.")

    def _conduct_list_rite(self, model_dir: Path) -> ScaffoldResult:
        """Lists all learned signatures."""
        signatures = [f.stem for f in model_dir.glob("*.json")]
        if not signatures:
            return self.success("No Gnostic Signatures have been learned in this sanctum.")

        table = Table(title="Enshrined Gnostic Signatures")
        table.add_column("Signature Name", style="cyan")
        for sig in sorted(signatures):
            table.add_row(sig)

        self.console.print(table)
        return self.success(f"Found {len(signatures)} enshrined signature(s).")