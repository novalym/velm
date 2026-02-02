# Path: scaffold/artisans/simulacrum/heuristics/strategies.py
# -----------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: @)(@(()@()@ | ROLE: GNOSTIC_DNA_REGISTRY
# =================================================================================
# == THE STRATEGY MATRIX (V-Ω-TOTALITY-FINAL-V3)                                 ==
# =================================================================================

import re
from dataclasses import dataclass, field
from typing import List, Dict, Pattern

@dataclass
class LanguageDNA:
    """The genetic markers and exclusion laws of a programming language."""
    name: str
    extensions: List[str]
    # Primary (Weight: 25): Definitive structural markers
    primary: List[str] = field(default_factory=list)
    # Secondary (Weight: 5): Supporting keywords
    secondary: List[str] = field(default_factory=list)
    # Forbidden (Weight: -100): Physically impossible in this language
    forbidden: List[str] = field(default_factory=list)
    # Structural (Weight: 50): Complex regex patterns
    structural: List[str] = field(default_factory=list)
    # Shebangs (Weight: 1000): Absolute Truth
    shebangs: List[str] = field(default_factory=list)

    def compile_structural(self) -> List[Pattern]:
        return [re.compile(p, re.MULTILINE) for p in self.structural]

# =================================================================================
# == THE POLYGLOT FOUNDRY (DNA DEFINITIONS)                                     ==
# =================================================================================

# --- 1. THE SERPENT (PYTHON) ---
PYTHON_DNA = LanguageDNA(
    name="python",
    extensions=[".py", ".pyw"],
    primary=["def ", "elif ", "from ", "raise ", "yield ", "__name__", "self.", "cls."],
    secondary=["import", "print", "class", "try", "except", "return", "True", "False", "None"],
    # [ELEVATION 1]: Python cannot have semicolons at line end or braces for blocks
    forbidden=[r"{\s*$", r"};\s*$", r"const\s+", r"let\s+", r"interface\s+", r"function\s+"],
    structural=[
        r"^def\s+\w+\(.*\):",
        r"^class\s+\w+(\(.*\))?:",
        r"if\s+__name__\s*==\s*['\"]__main__['\"]:",
        r"from\s+[\w\.]+\s+import",
        r"@\w+\ndef\s+" # Decorator preceding a def
    ],
    shebangs=["python", "python3"]
)

# --- 2. THE LATTICE (TYPESCRIPT) ---
TYPESCRIPT_DNA = LanguageDNA(
    name="typescript",
    extensions=[".ts", ".tsx"],
    # [ELEVATION 2 & 3]: Braced imports and Type aliases
    primary=["import {", "export const", "export default", "interface ", "type ", "enum ", "readonly ", "public ", "private "],
    secondary=["function", "const", "let", "var", "import", "export", "class", "return", "await", "async"],
    forbidden=[r"def\s+\w+:", r"elif\s+", r"from\s+[\w\.]+\s+import"],
    structural=[
        r":\s*(string|number|boolean|any|void|Promise<|Record<)", # Type annotations
        r"interface\s+\w+\s*\{",
        r"import\s+\{.*\}\s+from",
        r"export\s+type\s+\w+",
        r"=>\s*\{", # Arrow functions
        r"as\s+(const|string|number|any)" # Type casting
    ],
    shebangs=["ts-node", "bun", "deno"]
)

# --- 3. THE SCRIPT (JAVASCRIPT) ---
JAVASCRIPT_DNA = LanguageDNA(
    name="javascript",
    extensions=[".js", ".jsx", ".mjs", ".cjs"],
    primary=["module.exports", "require(", "process.env", "document.", "window.", "console.log"],
    secondary=["function", "const", "let", "var", "import", "export", "class", "return", "await"],
    forbidden=[r"def\s+\w+:", r"elif\s+", r":\s*string\b", r":\s*number\b"],
    structural=[
        r"const\s+\w+\s*=\s*require\(",
        r"import\s+.*\s+from\s+['\"]",
        r"export\s+default\s+",
        r"\.map\(.*=>",
        r"\$\{.*\}", # Template literals
    ],
    shebangs=["node", "nodejs"]
)

# --- 4. THE IRON CORE (RUST) ---
RUST_DNA = LanguageDNA(
    name="rust",
    extensions=[".rs"],
    primary=["fn ", "let mut", "impl ", "struct ", "enum ", "mod ", "pub ", "crate ", "match ", "unwrap()", "expect("],
    secondary=["use", "return", "if", "else", "for", "while", "loop", "match"],
    forbidden=[r"def\s+\w+:", r"function\s+", r"var\s+"],
    structural=[
        r"fn\s+\w+\s*\(.*\)\s*->\s*", # Function with return type
        r"println!\(",
        r"vec!\[",
        r"pub\s+struct\s+\w+",
        r"impl\s+\w+\s+for\s+\w+",
        r"\w+::\w+" # Namespacing
    ],
    shebangs=["rust-script", "cargo"]
)

# --- 5. THE CLOUD (GO) ---
GO_DNA = LanguageDNA(
    name="go",
    extensions=[".go"],
    primary=["func ", "package ", "go ", "defer ", "chan ", "map[", "interface{}", ":="],
    secondary=["import", "return", "if", "else", "var", "const", "struct", "type"],
    forbidden=[r"def\s+\w+:", r"function\s+", r"{\s*$", r"let\s+"],
    structural=[
        r"func\s+\w+\(.*\)\s*\(?.*\)?\s*\{",
        r"package\s+main",
        r"fmt\.Print",
        r"go\s+func\(.*\)\s*\{",
        r"if\s+err\s*!=\s*nil" # The quintessential Go pattern
    ],
    shebangs=["go"]
)

# --- 6. THE KINETIC (SHELL) ---
SHELL_DNA = LanguageDNA(
    name="shell",
    extensions=[".sh", ".bash", ".zsh"],
    primary=["echo ", "ls ", "cd ", "grep ", "awk ", "sed ", "export ", "source ", "chmod ", "chown "],
    secondary=["if", "fi", "then", "else", "case", "esac", "while", "until", "for", "do", "done"],
    forbidden=[r"def\s+\w+:", r"function\s+\w+\(\)\s*{", r"import\s+"],
    structural=[
        r"^\s*#!",
        r"\w+=\$\(.*\)", # Command substitution
        r"if\s+\[\s+.*\s+\]",
        r"\|\s*grep\s+"
    ],
    shebangs=["bash", "sh", "zsh", "bin/sh", "bin/bash"]
)

# --- THE UNIFIED REGISTRY ---
# Order matters: Specificity is prioritized (e.g., TS before JS)
ALL_DNA = [
    RUST_DNA,
    GO_DNA,
    TYPESCRIPT_DNA,
    JAVASCRIPT_DNA,
    PYTHON_DNA,
    SHELL_DNA
]