# Path: scaffold/core/ignition/diviner/seekers/magic_seeker.py
# -----------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_MAGIC_SEEKER_V7

from pathlib import Path
from typing import Optional
from .base import BaseSeeker


class MagicSeeker(BaseSeeker):
    """
    =============================================================================
    == THE MAGIC-NUMBER SEEKER (V-Ω-DEEP-PACKET-INSPECTION)                    ==
    =============================================================================
    [ASCENSION 4]: Peeks at file headers to determine type without extensions.
    """

    # [FACULTY 4]: MAGIC SIGNATURES
    SIGNATURES = {
        b'#!/usr/bin/env python': 'python',
        b'#!/bin/bash': 'shell',
        b'#!/bin/sh': 'shell',
        b'<?php': 'php',
        b'<!DOCTYPE html>': 'html',
    }

    def scan(self, target: Optional[Path] = None) -> Optional[Path]:
        """
        Scans top-level files for Shebangs or HTML markers to identify a root.
        """
        curr = target or self.root

        for item in self.safe_iter(curr):
            if item.is_file() and item.stat().st_size > 0:
                try:
                    with open(item, 'rb') as f:
                        header = f.read(128)
                        for sig, aura in self.SIGNATURES.items():
                            if header.startswith(sig):
                                # If we find a shebang in the root, it's a strong indicator.
                                return curr
                except:
                    continue

        return None

