# Path: core/alchemist/elara/library/system_rites/network_http.py
# ---------------------------------------------------------------

import urllib.request
import urllib.parse
import json
import socket
import subprocess
import time
import platform
from typing import Any, Optional, Dict
from ..registry import register_rite
from ......logger import Scribe

Logger = Scribe("SystemRites:Network")

@register_rite("fetch")
def celestial_fetch(value: Any, url: Optional[str] = None, **kwargs) -> str:
    """[ASCENSION 7]: Downloads raw matter from the aether natively."""
    target_url = url if url else str(value)
    Logger.info(f"🛰️ [CELESTIAL FETCH] Inhaling matter from: {target_url}")
    try:
        headers = {'User-Agent': 'Velm-God-Engine/3.0'}
        req = urllib.request.Request(target_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10.0) as response:
            return response.read().decode('utf-8', errors='replace')
    except Exception as e:
        Logger.error(f"Celestial Fetch Fractured: {e}")
        return f"/* FETCH_FAILED: {str(e)} */"

@register_rite("http_get")
def http_get_rite(value: Any, **kwargs) -> Dict[str, Any]:
    """[ASCENSION 72]: Native JSON HTTP GET without requests library."""
    target_url = str(value)
    try:
        req = urllib.request.Request(target_url, headers={'User-Agent': 'Velm/3.0'})
        with urllib.request.urlopen(req, timeout=5.0) as res:
            data = res.read().decode('utf-8')
            try: return {"status": res.status, "data": json.loads(data)}
            except: return {"status": res.status, "data": data}
    except Exception as e:
        return {"status": 500, "error": str(e)}

@register_rite("http_post")
def http_post_rite(value: Any, payload: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """[ASCENSION 72]: Native JSON HTTP POST."""
    target_url = str(value)
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(target_url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Velm/3.0'}, method='POST')
        with urllib.request.urlopen(req, timeout=5.0) as res:
            resp_data = res.read().decode('utf-8')
            try: return {"status": res.status, "data": json.loads(resp_data)}
            except: return {"status": res.status, "data": resp_data}
    except Exception as e:
        return {"status": 500, "error": str(e)}

@register_rite("wait_for_port")
def temporal_port_vigil(value: Any, port: Optional[int] = None, timeout: int = 30, **kwargs) -> bool:
    target_port = int(port if port else value)
    start_time = time.time()
    Logger.info(f"⏳ [PORT VIGIL] Awaiting resonance on port {target_port}...")
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            if s.connect_ex(('127.0.0.1', target_port)) == 0:
                Logger.success(f"✅ Port {target_port} is RESONANT.")
                return True
        time.sleep(1.0)
    return False

@register_rite("port_open")
def is_port_open(value: Any, port: Optional[int] = None, **kwargs) -> bool:
    target_port = int(port if port else value)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.1)
        return s.connect_ex(('127.0.0.1', target_port)) == 0

@register_rite("free_port")
def find_open_aperture(value: Any = None, start: int = 8000, end: int = 9000) -> int:
    try: current_port = int(value) if str(value).isdigit() else int(start)
    except: current_port = int(start)
    while current_port <= end:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', current_port)) != 0:
                return current_port
        current_port += 1
    raise OSError(f"Topological Exhaustion: No free ports waked in range {start}-{end}.")

@register_rite("ping")
def ping_host(value: Any, count: int = 1, **kwargs) -> float:
    """[ASCENSION 76]: Achronal Ping to measure latency."""
    host = str(value)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        start = time.perf_counter()
        subprocess.run(["ping", param, str(count), host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        return round((time.perf_counter() - start) * 1000 / count, 2)
    except:
        return 9999.9