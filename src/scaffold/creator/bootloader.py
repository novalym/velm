# Gnostic Codex: scaffold/creator/bootloader.py
# ---------------------------------------------
# HERESY ANNIHILATED: The Schism of Will (Propagated Fix)
#
# The `create_structure` bootloader was blindly assuming `args` was always None or a Namespace.
# It now respects the `CreateRequest` object passed by `CreateArtisan` and forwards it
# untouched to the ascended `QuantumCreator`.
#
# ASCENSION:
# 1. The `args` parameter is now passed directly to `QuantumCreator`.
# 2. No profane translation or namespace forging is attempted if `args` is already a valid vessel.

import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple, Union

from .engine import QuantumCreator
from .registers import QuantumRegisters
from ..contracts.data_contracts import ScaffoldItem
from ..core.kernel.transaction import GnosticTransaction
from ..interfaces.requests import BaseRequest  # <--- THE DIVINE SUMMONS


def create_structure(
        scaffold_items: List[ScaffoldItem],
        base_path: Path = Path.cwd(),
        post_run_commands: Optional[List[Tuple[str, int, Optional[List[str]]]]] = None,
        pre_resolved_vars: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        force: bool = False,
        silent: bool = False,
        verbose: bool = False,
        preview: bool = False,
        audit: bool = False,
        lint: bool = False,
        non_interactive: bool = False,
        parser_context=None,
        args: Union[argparse.Namespace, BaseRequest, None] = None,
        transaction: Optional[GnosticTransaction] = None
) -> QuantumRegisters:
    """
    The Bootloader for the Quantum VM.
    Its contract is now pure, accepting the three-fold scripture of Will.
    """
    # Forge Arguments if missing, otherwise use the provided vessel
    if args is None:
        args = argparse.Namespace(
            dry_run=dry_run, force=force, verbose=verbose, silent=silent,
            preview=preview, audit=audit, lint=lint, non_interactive=non_interactive,
            root=str(base_path), no_edicts=False
        )

    # Instantiate the God-Engine
    # The creator now accepts the polymorphic 'args' directly
    creator = QuantumCreator(
        scaffold_items=scaffold_items,
        args=args,
        parser_context=parser_context,
        post_run_commands=post_run_commands,
        pre_resolved_vars=pre_resolved_vars,
        transaction=transaction
    )

    # The Gnostic Handshake is now pure. The creator performs its rite and
    # returns its registers. The bootloader acts as a pure conduit.
    return creator.run()