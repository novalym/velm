# Path: core/lsp/rpc/filters.py
# -----------------------------

from typing import Dict, Any, Set

# [ASCENSION 4]: THE O(1) SIEVE
METABOLIC_NOISE: Set[str] = {
    '$/heartbeat',
    'heartbeat',
    'ping',
    'pong',
    'scaffold/progress',
    'window/logMessage',
    '$/progress'
}


def is_metabolic_noise(payload: Dict[str, Any]) -> bool:
    """Divines if a packet is purely biological maintenance."""
    method = payload.get('method')
    if method in METABOLIC_NOISE:
        return True

    # [ASCENSION 11]: Shadow-Status Triage
    if payload.get('command') == 'shadow':
        params = payload.get('params', {})
        if params.get('shadow_command') == 'status':
            return True

    return False