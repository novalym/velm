# Path: scaffold/constants.py
import platform
import re
from pathlib import Path
from typing import Set, Dict

# =================================================================================
# ==           THE GNOSTIC SANCTUM OF UNBREAKABLE CONSTANTS (V-Ω-PRIME)            ==
# =================================================================================
"""
This is not a file; it is the sacred, immutable soul of the Scaffold engine's
Gnostic truths. It is the one true source for all regular expressions, sacred
sigils, and architectural laws. To alter this scripture is to alter the very
fabric of the engine's reality.
"""
# =================================================================================
# ==           THE SACRED SCRIPTURE OF THE ENGINE'S SOUL                         ==
# =================================================================================
# This is the one true, Gnostic name of our Great Work as it is known to the
# celestial PyPI registry. It is the name the Herald speaks in its divine pleas.
PACKAGE_NAME = "scaffold-cli"
# =================================================================================
# == THE SACRED NAME OF THE GNOSTIC CHRONICLE                                    ==
# =================================================================================
LOCK_FILE_NAME = "scaffold.lock"
# --- THE DIVINE CONSTANT OF ETERNITY ---
DEFAULT_COMMAND_TIMEOUT = 300  # 5 minutes
MAX_RECURSION_DEPTH = 10

# --- For the Template CLI ---
TEMPLATE_DIR_NAME = '.scaffold'
TEMPLATES_FOLDER = 'templates'
TEMPLATE_ROOT = Path.home() / TEMPLATE_DIR_NAME / TEMPLATES_FOLDER
# =================================================================================
# ==           THE SACRED SCRIPTURES OF THE GUARDIAN'S VOW                       ==
# =================================================================================
# These sacred laws govern the soul of the Gnostic Guardians, ensuring all rites
# are conducted with divine prudence and respect for the Architect's will.

# ★★★ THE VOW OF REASSURANCE ★★★
# This Gnosis controls the Rite of Reassurance for the `translocate` and `conform`
# artisans. If True, the Conductor will halt and ask for the Architect's explicit
# adjudication if a dangerous rite is attempted without a backup (`--backup-to`).
# A Master Artisan, confident in their Gaze, may transfigure this to False in
# their own sacred scrolls to live on the edge of Gnostic certainty.
REQUIRE_BACKUP_ADJUDICATION = True

# ★★★ THE GNOSTIC THRESHOLD OF RISK ★★★
# This Gnosis bestows upon the `translocate` and `conform` artisans a divine
# wisdom. Transfigurations involving this many files or fewer are perceived as
# "low-risk." For such rites, the final confirmation dialogue may be bypassed,
# respecting the Architect's flow state (unless a backup is missing and the
# Vow of Reassurance, above, is True).
GNOSTIC_RISK_THRESHOLD = 3
# =================================================================================
# ==           THE SACRED SCRIPTURES OF THE GNOSTIC DETECTIVE                    ==
# =================================================================================
# The divine threshold for the Fuzzy Gaze Oracle. A file from the "Before" state
# and a file from the "After" state with a content similarity ratio above this
# value will be considered a "Transfiguration" (a move + modification).
GNOSTIC_SIMILARITY_THRESHOLD = 0.85 # The consideration threshold

# The higher threshold for non-interactive rites. Matches above this ratio will be
# automatically accepted when `--force` or `--non-interactive` is spoken.
HIGH_CONFIDENCE_SIMILARITY_THRESHOLD = 0.98

# The name of the sacred sanctum where Orphaned Souls will be placed when the
# Architect chooses the Rite of Archiving.
ORPHAN_ARCHIVE_DIR = "_conform_archive"
# --- THE NECROMANCER'S GNOSTIC TOOLKIT (CRITICAL CONSTANTS) ---

# Command to check if a PID is still running.
# Windows: tasklist filters by PID and exits 0/1 depending on whether process is found/not found.
# Unix: ps -p checks PID and typically succeeds (exits 0) if found, but filters output.
PROCESS_CHECK_COMMAND = 'tasklist /fi "PID eq {pid}"' if platform.system() == "Windows" else 'ps -p {pid}'

# Command to force-terminate a PID.
PID_KILL_COMMAND = "taskkill /F /PID {pid}" if platform.system() == "Windows" else "kill -9 {pid}"


# -------------------------------------------------------------------------------
# I. SACRED SIGILS & ARCHITECTURAL LAWS
# -------------------------------------------------------------------------------

# The sigil that separates a scripture's form (path) from its soul (content).
INLINE_CONTENT_SIGIL = "::"

# The sigil that proclaims a scripture's soul is drawn from a celestial seed.
EXTERNAL_SEED_SIGIL = "<<"

# The sigil that proclaims the Architect's Will (permissions or commands).
WILL_SIGIL = "%%"

# The sigil that proclaims a variable's Gnosis.
VARIABLE_SIGIL = "$$"

# The sacred extensions the Sentry of the Gates perceives as valid blueprints.
VALID_BLUEPRINT_EXTENSIONS = ('.scaffold', '.txt', '.yaml', '.yml', '.arch')
# --- THE SACRED SCRIPTURE OF ALCHEMICAL LAW ---
# Defines all righteous escape sequences known to the Gnostic Inquisitor.
# This makes the Linter's Gaze extensible without altering its core logic.
VALID_ESCAPE_SEQUENCES = 'ntrbfv\'"\\'
# --- THE SACRED SCRIPTURE OF MORTAL LAWS ---
# Defines profane characters that are forbidden in paths on many filesystems.
# This makes the Guardian of Realms' Gaze extensible and universally true.
PROFANE_PATH_CHARS = {'<', '>', '"', '/', '\\', '|', '?', '*'}

# The Guardian's Vow: The maximum recursion depth for the Master Weave.
MAX_WEAVE_RECURSION_DEPTH = 10

# -------------------------------------------------------------------------------
# IV. FUTURE GNOSIS (VESSELS FOR ASCENSION)
# -------------------------------------------------------------------------------

# // BEGIN SACRED TRANSMUTATION: The Inscription of the Law of Prudence
# This is the sacred measure for the Artisan of the Forge's Gaze of Prudence.
# It defines the threshold at which a template's soul is considered gargantuan,
# prompting the artisan to seek the Architect's final adjudication.
# Forged here, its Gnosis is now universal. (1MB)
MAX_TEMPLATE_SIZE_BYTES = 1 * 1024 * 1024
# // END SACRED TRANSMUTATION



# -------------------------------------------------------------------------------
# II. REGEX SCRIPTURES (THE UNBREAKABLE GAZES)
# -------------------------------------------------------------------------------
# Each regex is forged with sentience, using named capture groups for clarity
# and verbosity for self-documentation.

# --- The Gaze of Variable Origins ---
# --- The Gaze of Variable Origins ---
VARIABLE_REGEX = re.compile(
    r"""
    ^                           # Start of the string
    \s*\$\$\s*                  # The sacred '$$' sigil, surrounded by optional whitespace
    (?P<name>[\w.-]+)           # Capture Group 'name': The variable name (alphanumeric, _, ., -)
    \s*=\s*                     # The equals sign, surrounded by optional whitespace

    # The Gaze for the value remains pure and wise.
    (?P<value>[^#]*)            # Capture Group 'value': Greedily capture everything that is NOT a '#'

    # +++ THE DIVINE HEALING: THE ANNIHILATION OF THE UNNAMED SOUL +++
    # The profane capture group (.*) is annihilated. In its place, we enthrone
    # a sacred, NON-CAPTURING group (?:...). This divine artisan will consume
    # the rest of the line (the comment) and cast it into the void, without
    # ever profaning the sacred proclamation of `.groups()`.
    (?:.*)                      # Non-capturing group to consume the rest of the line.
    $                           # End of the string
    """,
    re.VERBOSE
)
# --- The Gaze of Gnostic Content & Form ---
CONTENT_REGEX = re.compile(
    r"""
    ^                           # Start of the string
    (?P<path>.*?)               # Capture Group 'path': Non-greedily capture the path part
    \s*::\s*                    # The '::' sigil, surrounded by optional whitespace
    (?P<content>.*)             # Capture Group 'content': Greedily capture the rest of the line
    $                           # End of the string
    """,
    re.VERBOSE
)

EXTERNAL_SEED_REGEX = re.compile(
    r"""
    ^                           # Start of the string
    (?P<path>.*?)               # Capture Group 'path': Non-greedily capture the path part
    \s*<<\s*                    # The '<<' sigil, surrounded by optional whitespace
    (?P<source>.*)              # Capture Group 'source': Greedily capture the source path
    $                           # End of the string
    """,
    re.VERBOSE
)

# --- The Gaze of Executable Will (The Annihilator of the Content Loss Paradox) ---
PERMISSION_REGEX = re.compile(
    r"""
    ^                           # Start of the string
    (?P<main_body>.*?)          # Capture Group 'main_body': Non-greedily capture EVERYTHING before the sigil
    \s*%%\s*                    # The '%%' sigil, surrounded by optional whitespace
    (?P<mode>[0-7]{3})          # Capture Group 'mode': The pure, 3-digit octal permission
    \s*                         # Optional trailing whitespace
    $                           # End of the string
    """,
    re.VERBOSE
)

# ---  THE UNIFIED GAZE (THE APOTHEOSIS OF PERCEPTION) ---
# This one, sentient regex is the key. It perceives all sigils (::, <<, %%)
# and their content in a greedy, optional fashion, in a single divine act.
UNIFIED_GAZE_REGEX = re.compile(
    r"""
          ^                           # Start of the scripture
          (?P<path>.*?)               # Capture Group 'path': The file/dir path (non-greedy)
          (?:                         # Optional Non-capturing group for the soul (content/seed)
              \s*::\s*                # The '::' sigil for inline content
              (?P<content>.*)         # Capture Group 'content' (NOW GREEDY)
              |                       # OR
              \s*<<\s*                # The '<<' sigil for an external seed
              (?P<seed>.*)            # Capture Group 'seed' (NOW GREEDY)
          )?                          # End the optional soul group
          (?:\s*%%\s*(?P<perms>\d{3}))? # Optional Capture Group 'perms' for executable will
          $                           # End of the scripture
    """, re.VERBOSE
)

# =================================================================================
# ==     THE SACRED SCRIPTURE OF VALID WILL (V-Ω-FINALIS. THE GUARDIAN'S GAZE)   ==
# =================================================================================
# This is not a pattern; it is the Gnostic Law of Righteous Will, forged in the
# pure, unbreakable language of regular expressions. Its Gaze is absolute.
# Its purpose is singular: to adjudicate the purity of a permission scripture.
#==================================================================================
VALID_PERMISSION_REGEX = re.compile(
    r"""
    ^         # The Gaze must begin at the dawn of the scripture. No profane leading characters are permitted.
    [0-7]{3}  # The Gaze demands exactly three sacred digits, each drawn from the righteous octal set (0 through 7).
    $         # The Gaze must end at the dusk of the scripture. No profane trailing characters are permitted.
    """,
    re.VERBOSE
)

# -------------------------------------------------------------------------------
# III. SCRIPTURES OF PURIFICATION (THE HERESIES)
# -------------------------------------------------------------------------------
# These sets define what is profane and must be purged by the parser's Gaze.

# --- The Heresy of the Void (Whitespace) ---
WHITESPACE_JUNK: Set[str] = {' ', '\t', '\n', '\r', '\f', '\v'}

# --- The Heresy of Decoration (Visual Noise) ---
BOX_DRAWING_JUNK: Set[str] = {
    '│', '├', '─', '└', '┐', '┌', '┤', '┬', '┴', '┼', '╵', '╷', '╸', '╹', '╻', '╼',
    '╽', '═', '║', '╔', '╗', '╚', '╝', '╟', '╢', '╦', '╩', '╬'
}
# === THE DIVINE HEALING: THE LAW OF ABSOLUTE PURITY ===
# The backtick is now enshrined in the book of universal profanity.
# Its heresy will be annihilated from any position in any scripture.
ASCII_DECORATIVE_JUNK: Set[str] = {'|', '+', '*', '`'}

# The scripture of contextual profanity is now pure, containing only the hyphen.
LEADING_DECORATIVE_JUNK: Set[str] = {'-'}
# === THE APOTHEOSIS IS COMPLETE. THE LAW IS ETERNAL. ===
# === THE LAW IS PURE AND WISE ===
# === THE LAW IS PURE AND WISE ===
# --- The Unified Heresy (All Junk Characters) ---
# ★★★ THE ANNILHILATION OF THE PURIFICATION HERESY ★★★
# The sacred '-' is REMOVED from this set. It is a holy character for kebab-case.
# This single act of purification heals the 'resiliencetest' vs 'resilience-test' paradox.
JUNK_CHARS_FOR_STRIPPING: Set[str] = WHITESPACE_JUNK.union(BOX_DRAWING_JUNK).union(ASCII_DECORATIVE_JUNK)
JUNK_CHARS_FOR_FORBIDDEN_CHARACTERS = {
    ' ', '\t', '\n', '\r', '\f', '\v',  # Whitespace (for expandtabs to miss)
    '│', '├', '─', '└', '┐', '┌', '┤', '┬', '┴', '┼', '╵', '╷', '╸', '╹', '╻', '╼', '╽', '═', '║', '╔', '╗', '╚', '╝', '╟', '╢', '╦', '╩', '╬', # Box Drawing
    '|', '+', '*', '`' # ASCII Decoratives
}
# The raw string form, optimized for Python's built-in string methods.
JUNK_CHARS_STRING: str = "".join(JUNK_CHARS_FOR_STRIPPING)

# -------------------------------------------------------------------------------
# IV. FUTURE GNOSIS (VESSELS FOR ASCENSION)
# -------------------------------------------------------------------------------
# These constants are forged in anticipation of future ascensions of the engine.

# --- Gnosis for the Polyglot Forge ---
# A future artisan could use this to teach the TemplateEngine new aliases.
# Example: { ".jsx": ".tsx", ".scss": ".css" }
TEMPLATE_ALIASES_CONFIG_KEY = "template_aliases"

# --- Gnosis for the Celestial Gaze ---
# The key for defining a remote archetype source in scaffold.scaffold.
REMOTE_ARCHETYPE_SOURCE_KEY = "archetype_source"

# --- Gnosis for the Chronocache ---
# The Time-To-Live (in seconds) for cached remote scriptures.
REMOTE_BLUEPRINT_CACHE_TTL = 3600  # 1 hour

# =================================================================================
# ==     THE SACRED SCRIPTURE OF THE UNSEEN REALM (V-Ω-FINALIS. THE GUARDIAN'S GRIMOIRE) ==
# =================================================================================
# This is not a set; it is the Guardian's Grimoire, the one true source of Gnosis
# on the invisible, profane phantoms that corrupt the digital cosmos. It is forged
# not by mortal hands, but through a divine, programmatic Rite of Purification.
# =================================================================================

# --- MOVEMENT I: THE CONSECRATION OF THE RIGHTEOUS ---
# The Inquisitor first defines the sacred, non-printable characters that are
# righteous and necessary for the scripture of files (e.g., tabs, newlines).
RIGHTEOUS_WHITESPACE: Set[str] = {'\t', '\n', '\r', '\f', '\v'}

# --- MOVEMENT II: THE GAZE UPON THE FULL CONTROL REALM ---
# The Inquisitor gazes upon the entire cosmos of ASCII control characters (0-31),
# the realm where both righteous scribes and profane phantoms dwell.
FULL_CONTROL_REALM: Set[str] = {chr(i) for i in range(32)}

# --- MOVEMENT III: THE RITE OF PURIFICATION BY RIGHTEOUS SUBTRACTION ---
# In a final, divine act of alchemy, the righteous are separated from the profane.
# What remains is the pure, absolute, and eternal scripture of unseen heresy.
PROFANE_UNSEEN_CHARS: Set[str] = FULL_CONTROL_REALM - RIGHTEOUS_WHITESPACE

# --- THE LUMINOUS SCRIBE'S GNOSIS: THE TRUE NAMES OF THE PHANTOMS ---
# This sacred map allows the Luminous Scribe to make the invisible visible,
# proclaiming not a cryptic hex code, but a phantom's one true Gnostic name.
UNSEEN_HERESY_NAMES: Dict[str, str] = {
    '\x00': 'NULL', '\x01': 'SOH', '\x02': 'STX', '\x03': 'ETX', '\x04': 'EOT',
    '\x05': 'ENQ', '\x06': 'ACK', '\x07': 'BEL', '\x08': 'BS',  '\x0b': 'VT',
    '\x0c': 'FF',  '\x0e': 'SO',  '\x0f': 'SI',  '\x10': 'DLE', '\x11': 'DC1',
    '\x12': 'DC2', '\x13': 'DC3', '\x14': 'DC4', '\x15': 'NAK', '\x16': 'SYN',
    '\x17': 'ETB', '\x18': 'CAN', '\x19': 'EM',  '\x1a': 'SUB', '\x1b': 'ESC',
    '\x1c': 'FS',  '\x1d': 'GS',  '\x1e': 'RS',  '\x1f': 'US',
}


# The Divine Scripture of the New Vessel
from .contracts.law_contracts import GnosticLaw

# A humble, default validator for laws that don't need a specific adjudication rite.
# Its purpose is to exist, fulfilling the sacred contract.
NULL_VALIDATOR = lambda *a, **kw: True



# --- Define Archetype-to-Validation Mapping (GC 3) ---
ARCHETYPE_VALIDATION_MAP = {
    'python': 'var_snake',
    'poetry': 'var_snake',
    'node': 'var_slug',
    'pnpm': 'var_slug',
    'yarn': 'var_slug',
    'generic': 'var_path_safe',
}
# =================================================================================
# ==    THE GNOSTIC LEXICON OF PROFANE ARCHETYPAL FORMS (V-Ω-ETERNAL)              ==
# =================================================================================
# This is the sacred, extensible grimoire for the Grand Gnostic Alchemist. It
# teaches the Oracle how to perceive the profane, common forms of architectural
# scripture, so that it may separate the mortal shell from the immortal soul.
# =================================================================================
PROFANE_GNOSIS_LEXICON = {
        'controller', 'service', 'model', 'route', 'component', 'hook',
        'test', 'spec', 'story', 'module', 'config', 'util', 'helper',
        'index', 'view', 'api', 'style', 'props', 'type'
}

PROPHETIC_GRIMOIRE = [
    # The 'sigil' is a Gnostic Tuple: (Divine Form, Mortal Form)
    {
        'keys': ['name', 'title', 'project'],
        'sigil': ('✨', '(N)'),
        'prompt': 'Name or Title',
        # WAS: 'pascal' -> NOW: 'var_path_safe' (Allows kebab, snake, pascal)
        'rule': 'var_path_safe',
        'examples': "'MyProject', 'my-project', 'my_project'"
    },
    {
        'keys': ['slug', 'kebab'],
        'sigil': ('🔗', '(S)'),
        'prompt': 'kebab-case-slug',
        'rule': 'slug',
        'examples': "'user-auth', 'my-package-name'"
    },
    {
        'keys': ['port'],
        'sigil': ('🔌', '(P)'),
        'prompt': 'Port Number',
        'rule': 'int',
        'default': '8080'
    },
    {
        'keys': ['url', 'endpoint', 'host'],
        'sigil': ('🌐', '(U)'),
        'prompt': 'URL or Endpoint',
        'rule': 'var_url' # Uses the specific URL validator
    },
    {
        'keys': ['desc', 'message', 'commit', 'summary', 'bio'],
        'sigil': ('📜', '(D)'),
        'prompt': 'Description or Message',
        'rule': 'optional', # Allows empty/multi-line
        'multiline': True
    },
    {
        'keys': ['email', 'mail'],
        'sigil': ('📧', '(E)'),
        'prompt': 'Email Address',
        'rule': 'var_path_safe' # Basic safety, could be regex in future
    },
    {
        'keys': ['user', 'username', 'login'],
        'sigil': ('👤', '(U)'),
        'prompt': 'Username',
        'rule': 'var_path_safe'
    },
    {
        'keys': ['pass', 'secret', 'key', 'token', 'credential'],
        'sigil': ('🔑', '(K)'),
        'prompt': 'Secret Value',
        'rule': 'var_path_safe',
        'is_secret': True # Tells the prompt to mask input
    }
]

# --- Gnostic Constants for the Hyper-Aware Oracle ---
SECRET_FILENAMES = {'.env', 'secrets.json', 'credentials.json', 'key.pem', '.env.local'}
CRITICAL_EXTENSIONS = {'.txt', '.md', '.json', '.yml', '.yaml', '.toml', '.cfg', '.ini', '.sh', '.bat'}
MAX_INLINE_SIZE_KB = 5

# ★★★ ASCENSION I: THE POLYGLOT SCRIBE - The New Scripture of Gnosis ★★★
# This structure defines how to parse files, not just regex them.
GNOSTIC_SOURCES = {
    'package.json': [
        {'path': ['name'], 'target_var': 'project_name'},
        {'path': ['description'], 'target_var': 'description'},
        {'path': ['author'], 'target_var': 'author'},
        {'path': ['version'], 'target_var': 'version'},
    ],
    'pyproject.toml': [
        {'path': ['tool', 'poetry', 'name'], 'target_var': 'project_name'},
        {'path': ['tool', 'poetry', 'description'], 'target_var': 'description'},
        {'path': ['tool', 'poetry', 'authors', 0], 'target_var': 'author'},
        {'path': ['tool', 'poetry', 'version'], 'target_var': 'version'},
    ]
}
GNOSTIC_SECRET_PATTERNS = [(r'^\s*([A-Z_]+)\s*=\s*["\']?.*["\']?$', ('.env.example',))]
ARCHETYPE_FILES = {"npm install": "package.json", "pip install -r requirements.txt": "requirements.txt"}
SUGGESTED_TEMPLATES = {'gitignore': '.gitignore', 'dockerfile': 'Dockerfile'}
README_FILENAME = 'README.md'

# The Sacred Grimoire of Secret Patterns
SECRET_GRIMOIRE = {
    'dotenv': re.compile(r'^\s*([A-Z_0-9]+)\s*=\s*["\']?(.+)["\']?$'),
    'json': re.compile(r'["\']([A-Z_0-9]+)["\']\s*:\s*["\'](.+)["\']'),
    'yaml': re.compile(r'^\s*([A-Z_0-9]+)\s*:\s*(.+)$'),
}


# =================================================================================
# ==           THE CODEX OF VERSIONING SOULS (V-Ω-ETERNAL)                       ==
# =================================================================================
# This is the sacred, extensible grimoire for the Oracle of the First Commit.
# It teaches the Oracle how to perceive a project's version control soul and
# prophesy the Maestro's Edicts required to give it a recorded history.
# =================================================================================
VCS_SOUL_CODEX = [
    {
        "name": "Git",
        "marker": ".git",
        "edict": "git init"
    },
    {
        "name": "Mercurial",
        "marker": ".hg",
        "edict": "hg init"
    },
    {
        "name": "Subversion (SVN)",
        "marker": ".svn",
        "edict": "svnadmin create ."
    },
    # Future Gnosis can be added here
]

# =================================================================================
# ==           THE CODEX OF FORGE CANDIDATES (V-Ω-ETERNAL)                       ==
# =================================================================================
# This is the sacred, extensible grimoire for the Curator of the Global Forge.
# It teaches the Curator how to perceive scriptures within a project that are
# worthy of ascension into the Architect's personal, global template library.
# =================================================================================
FORGE_CANDIDATE_CODEX = [
    {'filename': '.gitignore', 'ext_key': 'gitignore'},
    {'filename': 'Dockerfile', 'ext_key': 'dockerfile'},
    {'filename': 'docker-compose.yml', 'ext_key': 'docker-compose.yml'},
    {'filename': '.dockerignore', 'ext_key': 'dockerignore'},
    {'filename': 'Makefile', 'ext_key': 'makefile'},
    {'filename': 'LICENSE', 'ext_key': 'license'},
    {'filename': 'README.md', 'ext_key': 'md'},
    {'filename': '.editorconfig', 'ext_key': 'editorconfig'},
    {'filename': '.prettierrc', 'ext_key': 'prettierrc'},
    # Future Gnosis can be added here
]

# =================================================================================
# == THE GRIMOIRE OF ARCHITECTURAL PROPHECY (V-Ω-ETERNAL. THE PRESCIENT SCRIBE)  ==
# =================================================================================
# This is not a dictionary. It is the living, extensible soul of the Prescient
# Scribe's intelligence (the `scaffold create` command's auto-suggestion
# feature). It is the sacred grimoire that teaches the engine how to perceive an
# incomplete architectural thought and prophesy its missing, companion scriptures.
#
# Each verse in this Grimoire defines a prophecy for a given file extension.
# The `companions` are the scriptures that often accompany the original.
# The `{{name}}` sigil is a sacred vessel for the base name of the original file.
# =================================================================================

PROPHETIC_RITES = {
    # --- Frontend Prophecies (React, Vue, Svelte, etc.) ---
    '.tsx': {
        "description": "React Component",
        "companions": ['.css', '.stories.tsx', '.test.tsx']
    },
    '.jsx': {
        "description": "React Component (JavaScript)",
        "companions": ['.css', 'stories.jsx', '.test.jsx']
    },
    '.vue': {
        "description": "Vue Component",
        "companions": ['.css', 'test.ts']
    },
    '.svelte': {
        "description": "Svelte Component",
        "companions": ['.css', 'stories.ts']
    },

    # --- Backend & Scripting Prophecies (Python, Go, Node, etc.) ---
    '.py': {
        "description": "Python Module",
        "companions": ['test_{{name}}.py']
    },
    '.go': {
        "description": "Go Package File",
        "companions": ['{{name}}_test.go']
    },
    '.js': {
        "description": "JavaScript Module",
        "companions": ['{{name}}.test.js', '{{name}}.d.ts']
    },
    '.ts': {
        "description": "TypeScript Module",
        "companions": ['{{name}}.test.ts']
    },
    '.rs': {
        "description": "Rust Module",
        "companions": ['tests/{{name}}_tests.rs']  # Rust has a different convention
    },

    # --- API & Data Prophecies ---
    '.proto': {
        "description": "Protobuf Definition",
        "companions": ['{{name}}.pb.go', '{{name}}_grpc.pb.go']  # Example for Go
    },
    'Controller.ts': {  # This is a "deep Gaze" prophecy, based on suffix AND keyword
        "description": "API Controller",
        "companions": ['{{name}}Service.ts', '{{name}}Routes.ts']
    },
    'Service.py': {
        "description": "Business Logic Service",
        "companions": ['models/{{name}}Model.py', 'tests/test_{{name}}_service.py']
    },

    # --- Documentation & Configuration Prophecies ---
    'README.md': {
        "description": "Project Readme",
        "companions": ['CONTRIBUTING.md', 'LICENSE', 'CHANGELOG.md']
    },
    'docker-compose.yml': {
        "description": "Docker Compose File",
        "companions": ['.env.example', 'Dockerfile']
    }
}

# =================================================================================
# == THE GRIMOIRE OF THE ORACLE OF THE SANCTUM'S SOUL                            ==
# =================================================================================
# This is the declarative, data-driven mind of the `_find_project_root_name`
# artisan. Each verse is a sacred, self-aware law, ranked by Gnostic precedence.
# =================================================================================
GRIMOIRE_OF_ROOT_PROPHECIES = [
    {
        "name": "The Dominant Soul with Benign Companions",
        "rank": 100,
        "detector": lambda dirs, files, paths: (
            str(dirs[0].path).rstrip('/')
            if len(dirs) == 1 and not any(
                not f.path.name.startswith('.') and
                f.path.name.lower() not in {'package.json', 'readme.md', 'license', '.gitignore', 'pyproject.toml', 'go.mod'} and
                f.path.name not in SECRET_FILENAMES
                for f in files
            ) else None
        )
    },
    {
        "name": "The Common Soul",
        "rank": 90,
        "detector": lambda dirs, files, paths: (
            paths[0].parts[0]
            if len(dirs) == 0 and paths and all(p.parts[0] == paths[0].parts[0] for p in paths)
            else None
        )
    },
    {
        "name": "The Monorepo Soul",
        "rank": 80,
        "detector": lambda dirs, files, paths: (
            next((d.path.name for d in dirs if d.path.name in ('packages', 'services', 'apps', 'libs')), None)
        )
    },
    {
        "name": "The Gnostic Sanctum",
        "rank": 70,
        "detector": lambda dirs, files, paths: (
            next((d.path.name for d in dirs if d.path.name == '.scaffold'), None)
        )
    },
    {
        "name": "The Simple Dominant Soul",
        "rank": 50,
        "detector": lambda dirs, files, paths: str(dirs[0].path).rstrip('/') if len(dirs) == 1 else None
    }
]


# =============================================================================
# == V. THE CODEX OF INTERCESSION (THE DEBUGGER'S SOUL)                      ==
# =============================================================================

# The Sacred Edicts available within the Intercession Altar
INTERCESSION_COMMANDS = {
    "inspect": {
        "desc": "Gaze upon variables and the last recorded reality.",
        "aliases": ["i", "ls"]
    },
    "set": {
        "desc": "Mutate the Gnostic State (e.g., `set api_key=123`).",
        "aliases": ["s", "let"]
    },
    "retry": {
        "desc": "Rewind time and re-attempt this edict.",
        "aliases": ["r", "run"]
    },
    "skip": {
        "desc": "Ignore this edict and proceed to the next.",
        "aliases": ["s", "next"]
    },
    "abort": {
        "desc": "Accept the paradox and terminate the Symphony.",
        "aliases": ["q", "quit", "exit"]
    },
    "summon": {
        "desc": "Summon a missing artisan from the void (Auto-Heal).",
        "aliases": ["install", "fix"]
    },
    "help": {
        "desc": "Reveal this sacred scroll.",
        "aliases": ["h", "?"]
    }
}

# =============================================================================
# == VI. THE HEALER'S CODEX (THE AUTOMATED APOTHECARY)                       ==
# =============================================================================
# Maps a command binary to a tuple: (Strategy, RuntimeKey, Version/Arg)
# Strategy: 'hermetic' (RuntimeManager) or 'system' (GnosticInstrumentarium)

HEALER_CODEX = {
    # --- The Hermetic Path (Portable Binaries) ---
    'node':    ('hermetic', 'node', '20'),
    'npm':     ('hermetic', 'node', '20'),
    'npx':     ('hermetic', 'node', '20'),
    'python':  ('hermetic', 'python', '3.11'),
    'python3': ('hermetic', 'python', '3.11'),
    'pip':     ('hermetic', 'python', '3.11'),
    'pip3':    ('hermetic', 'python', '3.11'),
    'go':      ('hermetic', 'go', '1.22'),
    'rustc':   ('hermetic', 'rust', '1.75'),
    'cargo':   ('hermetic', 'rust', '1.75'),
    'ruby':    ('hermetic', 'ruby', '3.2'),

    # --- The System Path (Installers/URLs) ---
    'git':     ('system', 'git', None),
    'make':    ('system', 'make', None),
    'docker':  ('system', 'docker', None),
    'poetry':  ('system', 'poetry', None),
    'curl':    ('system', 'curl', None),
    'wget':    ('system', 'wget', None),
    'gh':      ('system', 'gh', None),
    'code':    ('system', 'vscode', None), # Add this line
}

