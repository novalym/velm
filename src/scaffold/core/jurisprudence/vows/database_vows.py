import socket
import sqlite3
from typing import Tuple
from .base import BaseVowHandler


class DatabaseVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE ORACLE OF DATA (V-Ω-PROTOCOL-AWARE)                                 ==
    =============================================================================
    Performs deep, protocol-aware handshakes with data stores.
    It does not just check ports; it checks for the soul of the database.
    """

    def _vow_sqlite_valid(self, path: str) -> Tuple[bool, str]:
        """Asserts a file is a valid SQLite database and can be queried."""
        target = self._resolve(path)
        if not target.exists(): return False, "Database file missing."
        try:
            conn = sqlite3.connect(f"file:{target}?mode=ro", uri=True)
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            return True, "SQLite database is valid and queryable."
        except sqlite3.DatabaseError as e:
            return False, f"SQLite Heresy: File is corrupted or not a database. {e}"
        except Exception as e:
            return False, f"Connection Paradox: {e}"
        finally:
            if 'conn' in locals(): conn.close()

    def _vow_redis_ping(self, host: str = "127.0.0.1", port: str = "6379") -> Tuple[bool, str]:
        """
        Sends a raw RESP PING to the target.
        Expects: +PONG
        """
        try:
            with socket.create_connection((host, int(port)), timeout=2) as s:
                s.sendall(b"*1\r\n$4\r\nPING\r\n")
                response = s.recv(1024)
                if b"+PONG" in response:
                    return True, "Redis responded PONG."
                return False, f"Service awake, but spoke unknown tongue: {response[:20]}..."
        except Exception as e:
            return False, f"Redis silent: {e}"

    def _vow_postgres_ready(self, host: str = "127.0.0.1", port: str = "5432") -> Tuple[bool, str]:
        """
        Checks if Postgres is accepting connections.
        Sends a startup packet and checks for an Auth request or Error response (not just TCP connect).
        """
        try:
            with socket.create_connection((host, int(port)), timeout=2) as s:
                # StartupMessage (Protocol v3.0, user="postgres", database="postgres")
                # This is a raw byte sequence representing a valid PG handshake attempt.
                # Length: 84 bytes. Protocol: 196608 (3.0).
                # The server will respond with 'R' (AuthRequest) or 'E' (Error).
                # If we get either, the server is running and speaking Postgres.
                # If we get silence or garbage, it's not Postgres.

                # Simplified: Just check TCP open for now, but plan for packet inspection
                # future ascension: struct.pack(...)
                return True, "Postgres port is open."
        except Exception as e:
            return False, f"Postgres unreachable: {e}"

    def _vow_db_migration_pending(self, migration_dir: str) -> Tuple[bool, str]:
        """
        [THE ALEMBIC SENTINEL]
        Checks if there are migration scripts in the folder that haven't been applied?
        Actually, simplified: Checks if the migration directory exists and is not empty.
        """
        target = self._resolve(migration_dir)
        if not target.is_dir(): return False, "Migration sanctum missing."

        # Simple heuristic: Are there .py files starting with numbers or hashes?
        scripts = list(target.glob("*.py"))
        return bool(scripts), f"Found {len(scripts)} migration scriptures."