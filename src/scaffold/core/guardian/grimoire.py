# Path: scaffold/core/guardian/grimoire.py
# ----------------------------------------

from .contracts import ThreatLevel

"""
=================================================================================
== THE BLACK GRIMOIRE & THE CROWN JEWELS                                       ==
=================================================================================
Static knowledge of what is dangerous and what is sacred.
"""

# Commands that are inherently dangerous
PROFANE_COMMANDS = {
    'rm': ThreatLevel.HIGH,
    'mv': ThreatLevel.MEDIUM,
    'dd': ThreatLevel.CRITICAL,
    'mkfs': ThreatLevel.CRITICAL,
    'fdisk': ThreatLevel.CRITICAL,
    'sudo': ThreatLevel.HIGH,
    'su': ThreatLevel.HIGH,
    'chown': ThreatLevel.HIGH,
    'chmod': ThreatLevel.MEDIUM,
    'wget': ThreatLevel.MEDIUM,
    'curl': ThreatLevel.MEDIUM,
    'nc': ThreatLevel.CRITICAL,
    'ncat': ThreatLevel.CRITICAL,
    'netcat': ThreatLevel.CRITICAL,
    'eval': ThreatLevel.CRITICAL,
    'exec': ThreatLevel.HIGH,
    ':(){:|:&};:': ThreatLevel.CRITICAL,  # Fork Bomb
}

# Files that MUST NEVER be touched by automated rites
CROWN_JEWELS = {
    # System
    "/etc/passwd", "/etc/shadow", "/etc/hosts", "/boot", "/proc", "/sys",
    "C:\\Windows", "C:\\Program Files",

    # Identity
    ".ssh", "id_rsa", "id_ed25519", "known_hosts",
    ".aws", ".kube", ".gnupg",

    # Project Identity
    ".git", ".env", ".env.production",
    "scaffold.lock",  # Only the Healer touches this
}

# Patterns that indicate potential injection or obfuscation
INJECTION_PATTERNS = [
    r"\$\(.*\)",  # Command substitution $()
    r"`.*`",  # Backticks
    r";\s*$",  # Trailing semi-colons
    r"\|\s*bash",  # Pipe to shell
    r"\|\s*sh",  # Pipe to shell
    r">\s*/dev/sd",  # Device writing
]