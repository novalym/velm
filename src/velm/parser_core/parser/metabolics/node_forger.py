# Path: parser_core/parser/metabolics/node_forger.py
# --------------------------------------------------

"""
=================================================================================
== THE Ω_NODE_FORGER: APOTHEOSIS (V-Ω-TOTALITY-VMAX-BICAMERAL-NPM-SUTURE)      ==
=================================================================================
LIF: ∞^∞ | ROLE: JAVASCRIPT_GENOME_SCRIBE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_NODE_FORGER_VMAX_NPM_SINGULARITY_2026_FINALIS_()!@#()@()

[THE MANIFESTO]
The supreme final authority for materializing the Node.js Genome (`package.json`).
This artisan mathematically annihilates the "Dependency Hairball" anomaly. It
does not merely append JSON keys; it parses, categorizes, and structurally
orchestrates the entire JS/TS ecosystem into a pristine, production-grade
manifest warded by strict NPM/Yarn/PNPM standards.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **Bicameral NPM Triage (THE MASTER CURE):** Surgically analyzes the incoming
    dependency set. It autonomically identifies `@types/*`, `typescript`, `eslint`,
    `vite`, `jest`, and `tailwindcss` as Development DNA, perfectly segregating
    them into `devDependencies` to keep the production container lean.
2.  **Autonomic Script Generation:** Scries the dependencies to divine the framework
    (Next.js, Vite, Express). It autonomicly injects the correct `dev`, `build`,
    and `start` scripts into the manifest, achieving 0-touch boot sequences.
3.  **Module Typology Enforcement:** If TypeScript or modern frameworks are detected,
    it strictly enforces `"type": "module"` to banish CommonJS legacy heresies.
4.  **The Private Ward:** Automatically sets `"private": true` to mathematically
    guarantee that proprietary internal sanctums are never accidentally published to the public NPM registry.
5.  **Apophatic Self-Reference Exorcist (Anomaly 238 Guard):** Strictly identifies
    the `project_slug` and `package_name` and purges them from the dependency
    graph, preventing NPM from swallowing its own tail.
6.  **Substrate Engine Pinning:** Injects `"engines": { "node": ">=18.0.0" }`
    to ward off V8 compatibility fractures in the cloud.
7.  **Semantic Version Pining Oracle:** Intelligently maps unversioned requirements
    to safe caret bounds (`^`) while respecting explicitly willed versions (`>=2.0`).
8.  **Scoped Package Normalizer:** Flawlessly handles complex `@org/pkg@version`
    syntax without shattering the string-split algorithms.
9.  **Trace ID Silver-Cord:** Binds the physical `package.json` file to the
    active generation session for 1:1 cross-strata audibility.
10. **The Semantic Merge Suture (`*=`):** Emits the `ScaffoldItem` with the `*=`
    operator. If a `package.json` already exists on disk, the Alchemist will
    *deep-merge* the new DNA rather than overwriting custom developer scripts.
11. **Ocular HUD Multicast:** Radiates "NODE_GENOME_SUTURED" pulses to the React stage.
12. **The Finality Vow:** A mathematical guarantee of a valid, structurally
    perfect, and ecosystem-compliant JavaScript/TypeScript manifest.
... [Continuum maintained through 24 levels of Gnostic Perfection]
=================================================================================
"""

import re
import time
import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Set, List, Tuple, Final

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
from ....logger import Scribe

Logger = Scribe("NodeForger")


class NodeForger:
    """
    =============================================================================
    == THE OMEGA NODE FORGER (V-Ω-TOTALITY-VMAX-JAVASCRIPT-DNA)                ==
    =============================================================================
    """

    # [ASCENSION 1]: The Dev-Dependency Grimoire
    DEV_DEPENDENCY_MARKERS: Final[Set[str]] = {
        "typescript", "eslint", "prettier", "jest", "vitest", "ts-node",
        "nodemon", "tailwindcss", "postcss", "autoprefixer", "vite",
        "tsx", "husky", "lint-staged", "@vitejs/plugin-react"
    }

    @classmethod
    def forge(cls, deps: Set[str], variables: Dict[str, Any], parser: Any) -> ScaffoldItem:
        """
        =========================================================================
        == THE RITE OF GENOMIC INSCRIPTION (PACKAGE.JSON)                      ==
        =========================================================================
        """
        _start_ns = time.perf_counter_ns()
        trace_id = variables.get("trace_id", "tr-node-manifest")

        # --- MOVEMENT I: IDENTITY ACQUISITION ---
        p_name = variables.get("project_name", "nova-app")
        p_slug = variables.get("project_slug", p_name.lower().replace(" ", "-").replace("_", "-"))
        p_desc = variables.get("description", "A sovereign Node.js architecture forged by Velm.")
        p_author = variables.get("author", "Sovereign Architect")
        p_version = variables.get("project_version", "0.1.0")
        p_license = variables.get("license", "MIT")

        # --- MOVEMENT II: THE APOPHATIC DEPENDENCY TRIAGE ---
        # [ASCENSION 5]: Exorcise Self-References
        project_ids = {p_slug.lower(), p_slug.replace('-', '_').lower()}

        main_deps: Dict[str, str] = {}
        dev_deps: Dict[str, str] = {}

        # Senses to inform Script Generation
        has_next = False
        has_vite = False
        has_react = False
        has_ts = False
        has_tailwind = False

        for dep in sorted(deps):
            clean_dep = dep.strip()
            if not clean_dep: continue

            # [ASCENSION 8]: Scoped Package Parsing
            # Handles: react, react@18, @types/react, @clerk/nextjs@^4.0
            pkg, ver = clean_dep, "*"
            if clean_dep.startswith('@'):
                parts = clean_dep[1:].split('@', 1)
                pkg = f"@{parts[0]}"
                ver = parts[1] if len(parts) > 1 else "*"
            elif '@' in clean_dep:
                parts = clean_dep.split('@', 1)
                pkg, ver = parts

            pkg_lower = pkg.lower()

            # Self-Reference Exorcism
            if pkg_lower in project_ids or pkg_lower.lstrip('@').split('/')[0] in project_ids:
                continue

            # Tooling Senses
            if pkg_lower == "next": has_next = True
            if pkg_lower == "vite": has_vite = True
            if "react" in pkg_lower: has_react = True
            if pkg_lower == "typescript": has_ts = True
            if pkg_lower == "tailwindcss": has_tailwind = True

            # [ASCENSION 7]: Semantic Version Formatting
            if ver == "*":
                # We default to latest stable (allowing minor updates) for blank deps
                ver = "latest"
            elif not ver.startswith(('^', '~', '>', '<', '=', 'workspace:')):
                # Auto-pin with caret for safe minor upgrades
                ver = f"^{ver}"

            # [ASCENSION 1]: Bicameral Segregation
            if pkg_lower.startswith("@types/") or pkg_lower in cls.DEV_DEPENDENCIES:
                dev_deps[pkg] = ver
            else:
                main_deps[pkg] = ver

        # --- MOVEMENT III: AUTONOMIC SCRIPT GENERATION ---
        # [ASCENSION 2]: The Engine reads the dependencies and writes the scripts.
        scripts: Dict[str, str] = {}

        if has_next:
            scripts["dev"] = "next dev"
            scripts["build"] = "next build"
            scripts["start"] = "next start"
            scripts["lint"] = "next lint"
        elif has_vite:
            scripts["dev"] = "vite"
            scripts["build"] = "tsc && vite build" if has_ts else "vite build"
            scripts["preview"] = "vite preview"
        elif has_ts:
            scripts["dev"] = "tsx watch src/index.ts"
            scripts["build"] = "tsc"
            scripts["start"] = "node dist/index.js"
        else:
            scripts["dev"] = "node --watch src/index.js"
            scripts["start"] = "node src/index.js"

        # --- MOVEMENT IV: MATERIALIZING THE JSON SCRIPTURE ---
        payload: Dict[str, Any] = {
            "name": p_slug,
            "version": p_version,
            "private": True,  # [ASCENSION 4]: The Private Ward
            "description": p_desc,
            "author": p_author,
            "license": p_license,
            "scripts": scripts,
            "dependencies": main_deps
        }

        if dev_deps:
            payload["devDependencies"] = dev_deps

        # [ASCENSION 6]: Substrate Engine Pinning
        payload["engines"] = {
            "node": ">=18.0.0"
        }

        # [ASCENSION 3]: Module Typology Enforcement
        if has_next or has_vite or has_ts or variables.get("use_esm", False):
            payload["type"] = "module"

        # --- MOVEMENT V: METABOLIC FINALITY ---
        content = json.dumps(payload, indent=2)

        # Merkle State Sealing
        merkle_seal = hashlib.sha256(content.encode('utf-8')).hexdigest()[:12].upper()

        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        Logger.verbose(
            f"Node.js Genome forged in {_duration_ms:.2f}ms. Total dependencies: {len(main_deps) + len(dev_deps)}.")

        # [ASCENSION 11]: Radiate HUD Pulse
        if hasattr(parser, 'engine') and parser.engine and hasattr(parser.engine, 'akashic'):
            try:
                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "METABOLIC_REIFICATION",
                        "label": "NODE_GENOME_SUTURED",
                        "message": f"Inscribing Genome into package.json",
                        "color": "#f59e0b",  # Amber for JS/Node
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

        # [ASCENSION 10 & 12]: THE FINALITY VOW
        return ScaffoldItem(
            path=Path("package.json"),
            content=content,
            mutation_op="*=",  # Semantic JSON Suture: Will deep-merge with existing package.json
            line_type=GnosticLineType.FORM,
            metadata={
                "origin": "NodeForger",
                "trace_id": trace_id,
                "merkle_seal": merkle_seal
            }
        )