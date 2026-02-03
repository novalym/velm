import httpx
from threading import Lock
from typing import Optional

class GlobalConnectionPool:
    """
    [THE ETHERIC GATE]
    A thread-safe, persistent connection pool for high-performance networking.
    Keeps TCP connections alive to reduce latency on repeated calls.
    """
    _instance: Optional[httpx.Client] = None
    _lock = Lock()

    @classmethod
    def get_client(cls) -> httpx.Client:
        with cls._lock:
            if cls._instance is None or cls._instance.is_closed:
                # We configure a robust client with reasonable limits
                cls._instance = httpx.Client(
                    timeout=30.0,
                    limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
                    follow_redirects=True
                )
            return cls._instance

    @classmethod
    def close(cls):
        with cls._lock:
            if cls._instance:
                cls._instance.close()
                cls._instance = None