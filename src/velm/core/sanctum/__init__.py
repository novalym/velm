# Path: src/velm/core/sanctum/__init__.py
# -------------------------------------

"""
=================================================================================
== THE SANCTUM PANTHEON (V-Ω-UNIVERSAL-SUBSTRATE-LAYER)                        ==
=================================================================================
LIF: ∞ | ROLE: REALITY_ABSTRACTION_LAYER | RANK: OMEGA_SOVEREIGN

This directory houses the God-Engines of I/O. Each Sanctum acts as a perfect
abstraction over a specific dimension of reality (Iron, Ether, Cloud, Wormhole).

They share a unified, unbreakable contract (`SanctumInterface`), allowing the
Architect to manipulate S3 buckets, SSH servers, and RAM disks as easily as
local files.
"""

from .contracts import SanctumStat, SanctumKind
from .base import SanctumInterface
from .local import LocalSanctum
from .memory import MemorySanctum
from .s3 import S3Sanctum
from .ssh import SSHSanctum
from .factory import SanctumFactory

__all__ = [
    "SanctumStat",
    "SanctumKind",
    "SanctumInterface",
    "LocalSanctum",
    "MemorySanctum",
    "S3Sanctum",
    "SSHSanctum",
    "SanctumFactory"
]