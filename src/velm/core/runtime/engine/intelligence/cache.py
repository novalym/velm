# Path: core/runtime/engine/intelligence/cache.py
# ----------------------------------------------

import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Any, Dict


class SmartCache:
    """
    =============================================================================
    == THE SMART CACHE (V-Ω-PERSISTENT-GNOSTIC-STORE)                          ==
    =============================================================================
    """

    def __init__(self, project_root: Path):
        self.cache_dir = project_root / ".scaffold" / "cache" / "intelligence"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, ttl_seconds: int = 3600) -> Optional[Any]:
        cache_file = self._get_path(key)
        if not cache_file.exists():
            return None

        try:
            data = json.loads(cache_file.read_text(encoding='utf-8'))
            if time.time() - data['timestamp'] > ttl_seconds:
                return None  # Expired
            return data['payload']
        except Exception:
            return None

    def set(self, key: str, payload: Any):
        cache_file = self._get_path(key)
        try:
            data = {
                "timestamp": time.time(),
                "payload": payload
            }
            cache_file.write_text(json.dumps(data), encoding='utf-8')
        except Exception:
            pass

    def _get_path(self, key: str) -> Path:
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.json"

