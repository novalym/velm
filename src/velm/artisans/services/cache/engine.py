import os
import json
import time
import redis
from typing import Any, Optional
from ....contracts.heresy_contracts import ArtisanHeresy

class RedisEngine:
    """[THE EPHEMERAL VAULT]"""
    _client = None

    @classmethod
    def get_client(cls):
        if not cls._client:
            url = os.environ.get("REDIS_URL", "redis://localhost:6379")
            cls._client = redis.from_url(url, decode_responses=True)
        return cls._client

    def execute(self, request) -> Any:
        r = self.get_client()
        k = request.key

        if request.action == "get":
            val = r.get(k)
            # Auto-deserialize JSON if it looks like structure
            if val and (val.startswith("{") or val.startswith("[")):
                try:
                    return json.loads(val)
                except:
                    pass
            return val

        elif request.action == "set":
            val = request.value
            if isinstance(val, (dict, list)):
                val = json.dumps(val)
            return r.set(k, val, ex=request.ttl)

        elif request.action == "delete":
            return r.delete(k)

        elif request.action == "exists":
            return bool(r.exists(k))

        elif request.action == "increment":
            # Atomic increment for rate limiting
            val = r.incrby(k, request.amount)
            if request.ttl:
                r.expire(k, request.ttl)
            return val

        elif request.action == "expire":
            return r.expire(k, request.ttl)

        elif request.action == "lock":
            # Distributed Lock Acquisition
            # Value is used as the Lock ID (usually UUID)
            lock_id = request.value or "locked"
            acquired = r.set(k, lock_id, nx=True, ex=request.ttl)
            if not acquired:
                # Simple spin-wait logic could go here, but for now we return False
                # allowing the caller to handle backoff
                return False
            return True

        elif request.action == "unlock":
            # Lua script to delete only if value matches (Safe Unlock)
            lua_script = """
            if redis.call("get",KEYS[1]) == ARGV[1] then
                return redis.call("del",KEYS[1])
            else
                return 0
            end
            """
            lock_id = request.value or "locked"
            return r.eval(lua_script, 1, k, lock_id)

        raise ValueError(f"Unknown Cache Action: {request.action}")