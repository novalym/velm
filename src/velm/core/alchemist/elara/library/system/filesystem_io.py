# Path: core/alchemist/elara/library/system_rites/filesystem_io.py
# ----------------------------------------------------------------

import os
import shutil
import time
import zipfile
from pathlib import Path
from typing import Any, List, Optional
from ..registry import register_rite
from ......logger import Scribe

Logger = Scribe("SystemRites:Filesystem")

@register_rite("mirror")
def resonant_mirror(value: Any, source_path: Optional[str] = None, **kwargs) -> str:
    """[ASCENSION 6]: Transmutes a physical directory into ELARA scripture JIT."""
    path_str = source_path if source_path else str(value)
    source_dir = Path(path_str).resolve()
    if not source_dir.exists() or not source_dir.is_dir(): return f"/* MIRROR_FAILED: '{path_str}' not found */"
    mirror_scripture =[]
    for root, dirs, files in os.walk(source_dir):
        dirs[:] =[d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'dist'}]
        for file in files:
            if file.endswith(('.pyc', '.lock', '.log')): continue
            abs_path = Path(root) / file
            rel_path = abs_path.relative_to(source_dir).as_posix()
            try:
                content = abs_path.read_text(encoding='utf-8', errors='ignore')
                mirror_scripture.append(f"{rel_path} :: \"\"\"\n{content}\n\"\"\"\n")
            except Exception: pass
    return "\n".join(mirror_scripture)

@register_rite("path_exists")
@register_rite("exists")
def gnostic_path_exists(value: Any) -> bool:
    path_str = str(value).strip().strip('"\'')
    if not path_str: return False
    try:
        p = Path(path_str)
        if p.exists(): return True
        if "*" in path_str or "?" in path_str:
            parent = p.parent if p.parent.exists() else Path(".")
            return len(list(parent.glob(p.name))) > 0
    except Exception: pass
    return False

@register_rite("list_dir")
def substrate_ls(value: Any) -> List[str]:
    p = Path(str(value).strip().strip('"\''))
    if not p.exists() or not p.is_dir(): return []
    return [f.name for f in p.iterdir()]

@register_rite("scry")
def deep_file_inquiry(value: Any, pattern: Optional[str] = None, lines: Optional[str] = None) -> str:
    path = Path(str(value).strip('"\''))
    if not path.exists() or not path.is_file(): return ""
    content = path.read_text(encoding='utf-8', errors='ignore')
    import re
    if lines:
        try:
            start, end = map(int, lines.split(':'))
            return "\n".join(content.splitlines()[start - 1:end])
        except: pass
    if pattern:
        matches = re.findall(str(pattern), content, re.MULTILINE)
        return "\n".join(matches) if matches else ""
    return content

@register_rite("patch")
def laminar_patch(value: Any, search: str, replace: str, count: int = 0) -> str:
    import re
    s = str(value)
    try: return re.sub(str(search), str(replace), s, count=int(count))
    except: return s.replace(str(search), str(replace))

@register_rite("walk")
def topographical_census(value: Any, pattern: str = "*", exclude: Optional[List[str]] = None) -> List[str]:
    root_path = Path(str(value).strip('"\''))
    if not root_path.exists() or not root_path.is_dir(): return[]
    default_exclude = {'.git', 'node_modules', '__pycache__', '.venv', 'scaffold.lock'}
    user_exclude = set(exclude) if exclude else set()
    total_exclude = default_exclude.union(user_exclude)
    file_list =[]
    for path in root_path.rglob(pattern):
        if not any(part in total_exclude for part in path.parts):
            if path.is_file():
                file_list.append(str(path.relative_to(root_path)).replace('\\', '/'))
    return sorted(file_list)

@register_rite("zip_dir")
def zip_dir_rite(value: Any, dest: str) -> bool:
    """[ASCENSION 68]: Substrate-Aware Archiving."""
    src_path = Path(str(value))
    dest_path = Path(dest)
    if not src_path.exists() or not src_path.is_dir(): return False
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(dest_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(src_path):
                for file in files:
                    file_path = Path(root) / file
                    zipf.write(file_path, file_path.relative_to(src_path))
        return True
    except Exception as e:
        Logger.error(f"Zip fracture: {e}")
        return False

@register_rite("unzip")
def unzip_rite(value: Any, dest: str) -> bool:
    """[ASCENSION 68]: Substrate-Aware Extraction."""
    src_path = Path(str(value))
    dest_path = Path(dest)
    if not src_path.exists() or not src_path.is_file(): return False
    try:
        dest_path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(src_path, 'r') as zipf:
            zipf.extractall(dest_path)
        return True
    except Exception as e:
        Logger.error(f"Unzip fracture: {e}")
        return False

@register_rite("chmod")
def chmod_rite(value: Any, perms: str) -> bool:
    """[ASCENSION 77]: Permission Normalizer."""
    try:
        p = Path(str(value))
        if not p.exists(): return False
        mode = int(str(perms), 8)
        p.chmod(mode)
        return True
    except: return False

@register_rite("chown")
def chown_rite(value: Any, user: str) -> bool:
    """[ASCENSION 78]: Ownership Projection (Safely ignores Windows)."""
    if os.name == 'nt': return True # Ward against windows crash
    try:
        import shutil
        shutil.chown(str(value), user=user)
        return True
    except: return False

@register_rite("symlink")
def symlink_rite(value: Any, dest: str) -> bool:
    """[ASCENSION 75]: Symlink Compatibility Suture."""
    src = Path(str(value)).resolve()
    dst = Path(dest)
    if not src.exists(): return False
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() or dst.is_symlink(): dst.unlink()
        os.symlink(src, dst)
        return True
    except OSError:
        # Fallback to copy if admin privileges missing on Windows
        try:
            if src.is_dir(): shutil.copytree(src, dst)
            else: shutil.copy2(src, dst)
            return True
        except: return False

@register_rite("watch_file")
def watch_file_rite(value: Any, timeout: int = 10) -> bool:
    """[ASCENSION 70]: Thread-Safe File Watching."""
    p = Path(str(value))
    if not p.exists(): return False
    start_mtime = p.stat().st_mtime
    start_time = time.time()
    while time.time() - start_time < timeout:
        if p.stat().st_mtime > start_mtime: return True
        time.sleep(0.5)
    return False