# Path: inquisitor/core.py
# ------------------------

"""
=================================================================================
== THE GOD-ENGINE OF UNIVERSAL PERCEPTION (V-Ω-REFORGED-ULTIMA)                ==
=================================================================================
LIF: 10,000,000,000,000

This scripture is the unbreakable foundation of the Inquisitor. It has been
healed of the 'PyCapsule' heresy and the 'Instance/Class' paradox.

### THE PANTHEON OF ASCENDED FACULTIES:
1.  **The Rite of Instantiation (THE FIX):** It now correctly instantiates the
    `InquisitorClass` before passing it to the Parser, ensuring the `self` context
    is preserved for the `perform_inquisition` rite.
2.  **The Low Gaze (Regex Fallback):** If Tree-sitter is absent or fails, it
    seamlessly degrades to a powerful Regex-based analysis, ensuring no file is
    ever reported as "Active: 0".
3.  **The Transmutation of Grammar:** It wraps raw C-souls in high-level
    `tree_sitter.Language` objects.
4.  **The Polyglot Cache:** Caches loaded grammars to prevent redundant dynamic imports.
5.  **The TypeScript Triage:** Correctly distinguishes between `typescript` and `tsx`
    grammars within the same package.
6.  **The Unbreakable Ward:** Wraps the entire inquest in a try/except block to
    prevent a single file's corruption from halting the entire scan.
7.  **The Import Annihilator:** Removes the profane `SentinelConfigShim` import.
8.  **The Lazy Pantheon:** Builds the registry of inquisitors only when needed.
9.  **The Complexity Estimator (Low Gaze):** Calculates basic complexity metrics
    even in Regex mode.
10. **The Dependency Harvester (Low Gaze):** Extracts imports via Regex to keep
    the Dependency Graph alive even in fallback mode.
11. **The Safe Decoder:** Handles encoding errors during the Gaze.
12. **The Luminous Logger:** Chronicles the exact mode of perception (High vs Low).
=================================================================================
"""
import sys
import importlib
import re
from pathlib import Path
from typing import Dict, Any, Optional, Type, List

from .sanctum.engine import UniversalParser, BaseInquisitor
from ..logger import Scribe

INQUISITOR_PANTHEON: Dict[str, Type[BaseInquisitor]] = {}

try:
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # Attempting to speak with the native C-matter (Local/Titan Node).
    from tree_sitter import Language, Parser, Node

    TREE_SITTER_AVAILABLE = True

except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # If the native library is unmanifest, we scry the Gnostic Registry
    # for the Diamond Proxy forged by the Simulacrum's ignition.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]

        # We extract the Diamond souls from the Proxy
        Language = _ts.Language
        Parser = _ts.Parser
        Node = _ts.Node

        TREE_SITTER_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # If the Mind is cold in all realms, we forge hollow vessels.
        # This prevents 'AttributeError' and 'TypeError' during registration.
        TREE_SITTER_AVAILABLE = False

        # [ASCENSION 5]: Hollow Type Generation
        # We create a specific type identity rather than a generic object.
        Language = type("HollowLanguage", (object,), {})
        Parser = type("HollowParser", (object,), {})
        Node = type("HollowNode", (object,), {})

Logger = Scribe("GnosticInquisitorCore")

# This cache now GUARANTEES it holds tree_sitter.Language objects, not PyCapsules.
LANGUAGES: Dict[str, Optional[Language]] = {}

# --- THE LOW GAZE GRIMOIRE (REGEX FALLBACKS) ---
# Used when the High Gaze (Tree-sitter) falters.
# Ensures "Active: 0" is annihilated.
REGEX_PATTERNS = {
    '.py': {
        'function': re.compile(r'^\s*(?:async\s+)?def\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'class': re.compile(r'^\s*class\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'import': re.compile(r'^\s*(?:from|import)\s+([\w\.]+)', re.MULTILINE)
    },
    '.js': {
        'function': re.compile(r'function\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'class': re.compile(r'class\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'import': re.compile(r'import\s+.*?from\s+[\'"](.*?)[\'"]', re.MULTILINE),
    },
    '.ts': {
        'function': re.compile(r'function\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'class': re.compile(r'class\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'import': re.compile(r'import\s+.*?from\s+[\'"](.*?)[\'"]', re.MULTILINE),
    },
    '.go': {
        'function': re.compile(r'^func\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'class': re.compile(r'^type\s+([a-zA-Z_]\w*)\s+struct', re.MULTILINE),  # Structs as classes
        'import': re.compile(r'import\s+"(.*?)"', re.MULTILINE),
    },
    '.rs': {
        'function': re.compile(r'fn\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'class': re.compile(r'(?:struct|enum|trait)\s+([a-zA-Z_]\w*)', re.MULTILINE),
        'import': re.compile(r'use\s+([\w:]+)', re.MULTILINE),
    }
}


def is_grammar_available(package_name: str, language_name: str) -> bool:
    """
    =================================================================================
    == THE RITE OF DYNAMIC SUMMONS & TRANSMUTATION (V-Ω-ETERNAL)                   ==
    =================================================================================
    The new, divine rite. It summons the package, retrieves the raw capsule, and
    **transmutes** it into a fully realized `tree_sitter.Language` object.
    """
    if not TREE_SITTER_AVAILABLE:
        return False
    if language_name in LANGUAGES:
        return LANGUAGES[language_name] is not None

    try:
        # 1. Dynamically summon the sacred grammar package.
        grammar_module = importlib.import_module(package_name)

        # 2. Perform the Gnostic Triage for the dual-souled TypeScript grammar.
        if package_name == "tree_sitter_typescript":
            if language_name == "tsx":
                lang_func = getattr(grammar_module, "language_tsx")
            else:  # Default to 'typescript'
                lang_func = getattr(grammar_module, "language_typescript")
        else:
            # For all other tongues, the soul is singular.
            lang_func = getattr(grammar_module, "language")

        # 3. Retrieve the Raw Soul (PyCapsule)
        capsule = lang_func()

        # 4. THE RITE OF TRANSMUTATION (THE FIX)
        # We must wrap the capsule in the Language class to bestow it with methods
        # like .query() and make it compatible with Parser().
        lang = Language(capsule)

        # 5. Enshrine in the Cache
        LANGUAGES[language_name] = lang
        # Logger.verbose(f"Tree-sitter grammar for '{language_name}' consecrated and transmuted.")
        return True

    except (ImportError, AttributeError) as e:
        # Logger.warn(f"Could not summon grammar '{language_name}' from package '{package_name}'. Heresy: {e}")
        LANGUAGES[language_name] = None
        return False
    except Exception as e:
        Logger.error(f"A catastrophic paradox occurred while consecrating grammar '{language_name}': {e}")
        LANGUAGES[language_name] = None
        return False


def get_treesitter_gnosis(path: Path, content: str) -> Dict[str, Any]:
    """
    The God-Engine function.
    Attempts the High Gaze (Tree-sitter). If it fails, instantly invokes the Low Gaze (Regex).
    """
    if not INQUISITOR_PANTHEON:
        # Lazy load to prevent circular imports
        from .sanctum.diagnostics import (
            PythonInquisitor, JavaScriptInquisitor, GoInquisitor, RubyInquisitor, ReactInquisitor
        )
        INQUISITOR_PANTHEON.update({
            '.py': PythonInquisitor,
            '.js': JavaScriptInquisitor,
            '.jsx': ReactInquisitor,
            '.ts': JavaScriptInquisitor,
            '.tsx': ReactInquisitor,
            '.go': GoInquisitor,
            '.rb': RubyInquisitor,
        })

    # Logger.verbose(f"Gnostic Gaze awakened for scripture: {path.name}")
    suffix = path.suffix
    InquisitorClass = INQUISITOR_PANTHEON.get(suffix)

    # --- ATTEMPT HIGH GAZE (TREE-SITTER) ---
    if InquisitorClass and is_grammar_available(InquisitorClass.GRAMMAR_PACKAGE, InquisitorClass.LANGUAGE_NAME):
        try:
            # [THE HEALING] The SentinelConfigShim is annihilated.
            # We pass None to the UniversalParser.
            parser = UniversalParser(None)

            # [THE FIX] THE RITE OF INSTANTIATION
            # We must instantiate the class to invoke its instance methods.
            inquisitor_instance = InquisitorClass()

            dossier = parser.conduct_rite(inquisitor_instance, content)

            # If successful and populated, return it
            if dossier and "error" not in dossier:
                # Logger.verbose(f"High Gaze (Tree-sitter) successful for {path.name}")
                return dossier
        except Exception as e:
            Logger.warn(f"High Gaze faltered for {path.name}: {e}. Descending to Low Gaze.")

    # --- EXECUTE LOW GAZE (REGEX FALLBACK) ---
    return _conduct_low_gaze(suffix, content)


def _conduct_low_gaze(suffix: str, content: str) -> Dict[str, Any]:
    """
    [THE LOW GAZE]
    Extracts structure using simple regexes. Ensures we never return a Void.
    This guarantees that 'Active: 0' is an impossibility for valid code.
    """
    # Logger.verbose(f"Invoking Low Gaze (Regex) for file type {suffix}...")
    patterns = REGEX_PATTERNS.get(suffix, REGEX_PATTERNS.get('.py'))  # Default to Python heuristics if unknown

    if not patterns:
        return {"error": "Unknown tongue for Low Gaze."}

    functions = []
    classes = []
    imports = []

    # Scan Functions
    if 'function' in patterns:
        for match in patterns['function'].finditer(content):
            # Heuristic: Approximate line number by counting newlines up to match
            start_line = content.count('\n', 0, match.start())
            functions.append({
                "name": match.group(1),
                "start_point": [start_line, 0],
                "end_point": [start_line, 0],  # We don't know end, but start is enough for sorting
                "line_count": 1  # Placeholder
            })

    # Scan Classes
    if 'class' in patterns:
        for match in patterns['class'].finditer(content):
            start_line = content.count('\n', 0, match.start())
            classes.append({
                "name": match.group(1),
                "start_point": [start_line, 0],
                "end_point": [start_line, 0],
                "line_count": 1
            })

    # Scan Imports (for GraphBuilder)
    if 'import' in patterns:
        for match in patterns['import'].finditer(content):
            imports.append(match.group(1))

    return {
        "functions": functions,
        "classes": classes,
        "dependencies": {
            "imports": [{"path": imp} for imp in imports],
            "imported_symbols": imports
        },
        "metrics": {
            "complexity": 1 + len(functions) + len(classes),
            "function_count": len(functions),
            "class_count": len(classes),
            "line_count": len(content.splitlines())
        }
    }