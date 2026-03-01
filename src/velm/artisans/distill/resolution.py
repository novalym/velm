import re
from typing import Union, Optional, Dict, List, Any

from ...core.cortex.contracts import DistillationProfile
from ...interfaces.requests import DistillRequest
from ...logger import Scribe

Logger = Scribe("DistillResolver")


class ArgumentResolver:
    """
    =================================================================================
    == THE ORACLE OF INTENT (V-Ω-SURGICAL-PRIMACY-ULTIMA)                          ==
    =================================================================================
    LIF: 100,000,000,000,000 | ROLE: ARCHITECTURAL_INTENT_TRANSMUTER

    The Sovereign Interpreter of the Architect's Will.
    It transmutes the raw `DistillRequest` into a purified `DistillationProfile`.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Apophatic Attribute Ward (THE CURE):** Every data extraction from the 
        Request vessel is now warded with `getattr(..., default)`, mathematically 
        annihilating the `AttributeError: object has no attribute 'depth'` heresy.
    2.  **The Law of Singular Intent:** Enforces the schism between `--focus` (Structure) 
        and `--intent` (Meaning). Focus triggers the Scalpel; Intent triggers Neural Search.
    3.  **The Surgical Primacy:** If `--focus` is detected, it automatically upgrades
        the strategy to `SURGICAL`, ensuring maximum fidelity for the target files
        while pruning the noise.
    4.  **The Profile Hydrator (Expanded):** Loads static configuration profiles 
        ('frontend', 'backend', 'data', 'forensic') to pre-populate filters and 
        traversal depths before applying CLI overrides.
    5.  **The Unified Exclusion:** Merges `ignore` patterns from the Profile, the CLI,
        and the Output Path itself (to prevent the Ouroboros heresy of reading the
        output file).
    6.  **The Budget Alchemist:** Safely parses both strings ('100k', '1.5m') and 
        integers into pure token counts, bridging CLI shorthand and Profile logic.
    7.  **The Causal Depth Link:** Safely bridges the `depth`, `include_dependents`, 
        and `include_dependencies` attributes into the Profile, unlocking the true 
        power of the Graph Traversal Engine.
    8.  **The Semantic Bridge:** Maps the `--intent` flag (and legacy `--feature`) 
        to the internal `feature` slot for the Semantic Engine.
    9.  **The Temporal & Forensic Link:** Passes `--since`, `--regression`, and 
        `--problem` flags to awaken the Chronomancer and the Inquisitor.
    10. **The Holographic Projector:** Maps the `dynamic_focus` (e.g. 'pytest') 
        to capture living coverage data during execution.
    11. **The Socratic Reviewer Toggle:** Configures `recursive_agent` for multi-pass
        AI refinement.
    12. **The Unbreakable Default:** Ensures a valid Profile is always returned, even
        from a void or profoundly malformed request.
    """

    @staticmethod
    def resolve_profile(profile_name: Optional[str]) -> Dict[str, Any]:
        """
        [FACULTY 4] The Profile Weaver.
        Loads static, domain-specific filter sets and traversal laws.
        """
        if not profile_name:
            return {}

        # The Grimoire of Pre-Defined Realities
        PROFILES = {
            "frontend": {
                "focus_keywords": ["component", "view", "route", "store", "ui", "props", "css", "scss", "tsx"],
                "ignore": ["*.py", "*.go", "**/__pycache__", "**/dist", "**/build", "**/coverage"],
                "depth": 2
            },
            "backend": {
                "focus_keywords": ["api", "route", "model", "schema", "db", "database", "service", "auth",
                                   "controller"],
                "ignore": ["*.js", "*.ts", "*.tsx", "*.css", "**/node_modules", "**/dist", "**/build"],
                "depth": 3
            },
            "data": {
                "focus_keywords": ["pipeline", "etl", "pandas", "numpy", "sql", "model", "train"],
                "ignore": ["**/node_modules", "*.css", "*.html"],
                "depth": 2
            },
            "forensic": {
                "strategy": "full",
                "depth": 5,  # Maximum Causal Depth
                "focus_keywords": ["error", "exception", "traceback", "handler", "logger", "crash", "panic"],
                "ignore": ["*.md", "*.txt", "docs/", "tests/"],
                "include_dependents": True,
                "include_dependencies": True
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
        =============================================================================
        == THE UNIFICATION RITE (V-Ω-ATTRIBUTE-WARDED)                             ==
        =============================================================================
        Merges Static Profiles, CLI Arguments, and Gnostic Logic into the Final Profile.
        Every access to the `request` object is warded with `getattr` to guarantee
        immunity against schema evolution and missing parameters.
        """
        # 1. Hydrate from Static Profile
        profile_key = getattr(request, 'profile', None)
        profile_data = ArgumentResolver.resolve_profile(profile_key)

        # 2. Gnostic Logic: The Strategy
        # Priority: CLI Request > Profile Default > System Default ('balanced')
        strategy = getattr(request, 'strategy', None) or profile_data.get('strategy', 'balanced')

        # 3. Gnostic Logic: The Focus Matrix & Surgical Primacy
        req_focus = getattr(request, 'focus', []) or []
        prof_focus = profile_data.get('focus_keywords', [])
        combined_focus = list(set(req_focus + prof_focus))

        # [FACULTY 3]: The Law of Surgical Primacy
        # If the Architect explicitly focuses on files, we assume they want deep
        # resolution of those files, not a broad, balanced scan.
        has_focus = bool(combined_focus)
        if has_focus and strategy == 'balanced':
            strategy = 'surgical'
            Logger.info("Focus detected. Upgrading strategy to [magenta]SURGICAL[/magenta] for precise extraction.")

        # 4. Gnostic Logic: The Intent (Prophecy I)
        # We merge --intent (new) and --feature (legacy) safely
        intent_query = getattr(request, 'intent', None) or getattr(request, 'feature', None)
        if intent_query:
            Logger.info(f"Intent perceived: [green]'{intent_query}'[/green]. Awakening Neural Cortex.")

        # 5. Gnostic Logic: The Exclusion Matrix (Ignore)
        req_ignore = getattr(request, 'ignore', []) or []
        prof_ignore = profile_data.get('ignore', [])
        combined_ignore = list(set(req_ignore + prof_ignore))

        # [FACULTY 5]: The Ouroboros Ward
        if output_name:
            combined_ignore.append(output_name)

        # 6. Gnostic Logic: The Inclusion Matrix
        req_include = getattr(request, 'include', []) or []
        prof_include = profile_data.get('include', [])
        combined_include = list(set(req_include + prof_include))

        # 7. Gnostic Logic: The Budget Alchemist (Tokens)
        # We parse the budget to ensure "100k" strings are cleanly converted to integers
        raw_budget = getattr(request, 'token_budget', None)
        if raw_budget is None:
            raw_budget = profile_data.get('token_budget', 100000)
        final_budget = ArgumentResolver._parse_budget(raw_budget)

        # 8. [THE CURE]: The Causal Physics (Graph Traversal Laws)
        # Safely extracting the depth and directional properties that were causing the AttributeError.
        final_depth = getattr(request, 'depth', profile_data.get('depth', 2))
        final_inc_dependents = getattr(request, 'include_dependents', profile_data.get('include_dependents', True))
        final_inc_dependencies = getattr(request, 'include_dependencies',
                                         profile_data.get('include_dependencies', True))
        final_trace_data = getattr(request, 'trace_data', profile_data.get('trace_data', []))

        # 9. Advanced Tracing & Telemetry
        final_dynamic_focus = getattr(request, 'dynamic_focus', profile_data.get('dynamic_focus', None))
        final_recursive_agent = getattr(request, 'recursive_agent', profile_data.get('recursive_agent', False))

        # 10. Forge the Immutable Vessel
        return DistillationProfile(
            # Economics & Strategy
            token_budget=final_budget,
            strategy=strategy,

            # Formatting & Purity
            strip_comments=strategy == 'aggressive',  # Aggressive mode naturally strips noise
            redact_secrets=getattr(request, 'redact_secrets', True),  # Always active by default
            redaction_level='mask',
            normalize_whitespace=True,

            # Spatial Targeting
            focus_keywords=combined_focus,
            feature=intent_query,  # Maps to Semantic Search
            ignore=combined_ignore,
            include=combined_include,
            stub_deps=getattr(request, 'stub_deps', []) or [],
            prioritize_tests=getattr(request, 'prioritize_tests', False),

            # Runtime Wraith (Dynamic State)
            trace_command=getattr(request, 'trace_command', None),
            snapshot_path=getattr(request, 'snapshot_path', None),
            profile_perf=getattr(request, 'profile_perf', False),
            dynamic_focus=final_dynamic_focus,

            # The Chronomancer (Temporal State)
            since=getattr(request, 'since', None),
            focus_change=getattr(request, 'focus_change', None),
            diff_context=getattr(request, 'diff_context', False),
            regression=getattr(request, 'regression', False),

            # The Inquisitors (Forensics & Security)
            problem_context=getattr(request, 'problem', None),
            audit_security=getattr(request, 'audit_security', False),
            scan_for_todos='summarize',

            # AI Governance
            no_ai=getattr(request, 'no_ai', False),
            interactive_mode=getattr(request, 'interactive', False),
            recursive_agent=final_recursive_agent,

            # Presentation & Diagrams
            lfg=getattr(request, 'lfg', False),
            summarize_arch=getattr(request, 'summarize_arch', False),
            summarize=getattr(request, 'summarize', False),

            # [ASCENSION 7]: GRAPH LOGIC (The Physics of Causality)
            depth=final_depth,
            include_dependents=final_inc_dependents,
            include_dependencies=final_inc_dependencies,
            trace_data=final_trace_data
        )

    @staticmethod
    def _parse_budget(v: Any) -> int:
        """
        [FACULTY 6]: THE ALCHEMIST OF NUMBERS
        A divine scribe that transmutes human-readable budget shorthands (e.g.,
        '800k', '1.5m') into their pure, integer soul (800000, 1500000).
        """
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            clean_v = v.lower().strip().replace(',', '')
            try:
                if clean_v.endswith('k'):
                    return int(float(clean_v[:-1]) * 1000)
                if clean_v.endswith('m'):
                    return int(float(clean_v[:-1]) * 1000000)
                return int(clean_v)
            except (ValueError, TypeError):
                Logger.warn(f"Profane budget string '{v}' detected. Falling back to 100,000.")
                return 100000

        # Absolute Fallback
        return 100000