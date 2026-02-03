# === [scaffold/artisans/distill/resolution.py] - SECTION 1 of 1: The Oracle of Intent ===
import re
from typing import Union, Optional, Dict, List, Any

from ...core.cortex.contracts import DistillationProfile
from ...interfaces.requests import DistillRequest
from ...logger import Scribe

Logger = Scribe("DistillResolver")


class ArgumentResolver:
    """
    =================================================================================
    == THE ORACLE OF INTENT (V-Ω-SURGICAL-PRIMACY)                                 ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign Interpreter of the Architect's Will.
    It transmutes the raw `DistillRequest` into a purified `DistillationProfile`.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Law of Singular Intent (Prophecy I):** It enforces the schism between
        `--focus` (Structure) and `--intent` (Meaning). Focus triggers the Scalpel;
        Intent triggers the Neural Search.
    2.  **The Surgical Primacy:** If `--focus` is detected, it automatically upgrades
        the strategy to `SURGICAL`, ensuring maximum fidelity for the target files
        while pruning the noise.
    3.  **The Profile Hydrator:** Loads static configuration profiles (e.g., 'frontend')
        to pre-populate filters before applying CLI overrides.
    4.  **The Unified Exclusion:** Merges `ignore` patterns from the Profile, the CLI,
        and the Output Path itself (to prevent the Ouroboros heresy of reading the
        output file).
    5.  **The Budget Alchemist:** Directs the Token Budget from the request to the profile.
    6.  **The Semantic Bridge:** Maps the new `--intent` flag to the internal `feature`
        slot for the Semantic Engine.
    7.  **The Legacy Ward:** Gracefully handles the deprecated `--feature` flag by
        merging it into the Intent stream.
    8.  **The Temporal Link:** Passes `--since` and `--regression` flags to activate
        the Chronomancer.
    9.  **The Runtime Bridge:** Forwards `--trace` and `--snapshot` to the Runtime Wraith.
    10. **The Forensic Channel:** Connects `--problem` to the Forensic Inquisitor.
    11. **The Visualizer's Toggle:** Configures the Logic Flow Graph (`lfg`) and
        Architectural Summary (`summarize_arch`) flags.
    12. **The Unbreakable Default:** Ensures a valid Profile is always returned, even
        from a void request.
    """

    @staticmethod
    def resolve_profile(profile_name: Optional[str]) -> Dict[str, Any]:
        """
        [FACULTY 3] The Profile Weaver.
        Loads static, domain-specific filter sets.
        """
        if not profile_name:
            return {}

        PROFILES = {
            "frontend": {
                "focus_keywords": ["component", "view", "route", "store", "ui", "props", "css", "scss", "tsx"],
                "ignore": ["*.py", "*.go", "**/__pycache__", "**/dist", "**/build", "**/coverage"]
            },
            "backend": {
                "focus_keywords": ["api", "route", "model", "schema", "db", "database", "service", "auth",
                                   "controller"],
                "ignore": ["*.js", "*.ts", "*.tsx", "*.css", "**/node_modules", "**/dist", "**/build"]
            },
            "data": {
                "focus_keywords": ["pipeline", "etl", "pandas", "numpy", "sql", "model", "train"],
                "ignore": ["**/node_modules", "*.css", "*.html"]
            }
        }

        profile_data = PROFILES.get(profile_name.lower())
        if profile_data:
            Logger.info(f"Applying Gnostic Profile: [bold cyan]{profile_name}[/bold cyan]")
            return profile_data

        Logger.warn(f"Unknown profile '{profile_name}'. The Gaze remains unguided.")
        return {}

    @staticmethod
    def forge_profile(request: DistillRequest, output_name: Optional[str]) -> DistillationProfile:
        """
        The Unification Rite.
        Merges Static Profiles, CLI Arguments, and Gnostic Logic into the Final Profile.
        """
        # 1. Hydrate from Static Profile
        profile_data = ArgumentResolver.resolve_profile(request.profile)

        # 2. Extract Request Data (The Architect's Will)
        # We exclude None values to allow Profile defaults to shine through
        request_data = request.model_dump(exclude_unset=True)

        # 3. Gnostic Logic: The Strategy
        strategy = request.strategy or profile_data.get('strategy', 'balanced')

        # [FACULTY 2] The Law of Surgical Primacy
        # If the Architect explicitly focuses on files, we assume they want deep
        # resolution of those files, not a broad, balanced scan.
        has_focus = bool(request.focus or profile_data.get('focus_keywords'))

        if has_focus and strategy == 'balanced':
            strategy = 'surgical'
            Logger.info("Focus detected. Upgrading strategy to [magenta]SURGICAL[/magenta] for precise extraction.")

        # 4. Gnostic Logic: The Intent (Prophecy I)
        # We merge --intent (new) and --feature (legacy)
        intent_query = request.intent or request.feature

        if intent_query:
            Logger.info(f"Intent perceived: [green]'{intent_query}'[/green]. Awakening Neural Cortex.")

        # 5. Gnostic Logic: The Exclusion Matrix
        # Merge ignores from Profile, Request, and the Output File itself.
        req_ignore = request.ignore or []
        prof_ignore = profile_data.get('ignore', [])

        combined_ignore = list(set(req_ignore + prof_ignore))

        # [FACULTY 4] The Ouroboros Ward
        if output_name:
            combined_ignore.append(output_name)

        # 6. Gnostic Logic: The Inclusion Matrix
        req_include = request.include or []
        prof_include = profile_data.get('include', [])
        combined_include = list(set(req_include + prof_include))

        # 7. Gnostic Logic: The Focus Matrix
        req_focus = request.focus or []
        prof_focus = profile_data.get('focus_keywords', [])
        combined_focus = list(set(req_focus + prof_focus))

        # 8. Forge the Immutable Vessel
        return DistillationProfile(
            # Economics
            token_budget=request.token_budget,
            strategy=strategy,

            # Formatting
            strip_comments=strategy == 'aggressive',  # Aggressive strips comments by default
            redact_secrets=True,  # Always active
            redaction_level='mask',
            normalize_whitespace=True,

            # Targeting
            focus_keywords=combined_focus,
            feature=intent_query,  # Maps to Semantic Search
            ignore=combined_ignore,
            include=combined_include,
            stub_deps=request.stub_deps or [],
            prioritize_tests=request.prioritize_tests,

            # Runtime Wraith
            trace_command=request.trace_command,
            snapshot_path=request.snapshot_path,
            profile_perf=request.profile_perf,

            # The Chronomancer
            since=request.since,
            focus_change=request.focus_change,
            diff_context=request.diff_context,
            regression=request.regression,

            # The Inquisitors
            problem_context=request.problem,
            audit_security=request.audit_security,
            scan_for_todos='summarize',

            # AI Governance
            no_ai=request.no_ai,
            interactive_mode=request.interactive,

            # Presentation
            lfg=request.lfg,
            summarize_arch=request.summarize_arch,
            summarize=request.summarize,

            # Graph Logic
            depth=request.depth,
            include_dependents=True,  # Default to true for context
            include_dependencies=True
        )