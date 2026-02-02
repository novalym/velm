# artisans/agent/Act/tools/file_system.py

from pathlib import Path
import os
import shutil
from .base import BaseTool
from .....utils import atomic_write


class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Writes content to a file. Creates directories if needed. Overwrites existing files."
    args_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Relative path to the file"},
            "content": {"type": "string", "description": "The full content to write"}
        },
        "required": ["path", "content"]
    }

    def execute(self, path: str, content: str) -> str:
        target = self.project_root / path
        if not target.resolve().is_relative_to(self.project_root.resolve()):
            return f"Error: Forbidden path '{path}'. Must be within project root."

        atomic_write(target, content, None, self.project_root, verbose=False)
        return f"Successfully wrote to {path}"


class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Reads the content of a file."
    args_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Relative path to the file"}
        },
        "required": ["path"]
    }

    def execute(self, path: str) -> str:
        target = self.project_root / path
        if not target.exists():
            return f"Error: File {path} does not exist."
        try:
            return target.read_text(encoding='utf-8')
        except Exception as e:
            return f"Error reading {path}: {e}"


class ListDirTool(BaseTool):
    name = "list_dir"
    description = "Lists files and directories recursively."
    args_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Relative path to the directory (default: root)"}
        }
    }

    def execute(self, path: str = ".") -> str:
        target = self.project_root / path
        if not target.exists() or not target.is_dir():
            return f"Error: {path} is not a directory."

        entries = []
        for root, dirs, files in os.walk(target):
            rel_root = Path(root).relative_to(target)
            for d in dirs:
                entries.append(str(rel_root / d) + "/")
            for f in files:
                entries.append(str(rel_root / f))

        return "\n".join(entries)


class MoveFileTool(BaseTool):
    name = "move_file"
    description = "Moves or renames a file or directory."
    args_schema = {
        "type": "object",
        "properties": {
            "source_path": {"type": "string", "description": "The original relative path."},
            "destination_path": {"type": "string", "description": "The new relative path."}
        },
        "required": ["source_path", "destination_path"]
    }

    def execute(self, source_path: str, destination_path: str) -> str:
        src = self.project_root / source_path
        dest = self.project_root / destination_path
        if not src.exists():
            return f"Error: Source path '{source_path}' not found."
        try:
            shutil.move(str(src), str(dest))
            return f"Successfully moved '{source_path}' to '{destination_path}'."
        except Exception as e:
            return f"Error moving file: {e}"


class DeleteFileTool(BaseTool):
    name = "delete_file"
    description = "Deletes a file. This action is irreversible."
    args_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "The relative path of the file to delete."}
        },
        "required": ["path"]
    }

    def execute(self, path: str) -> str:
        target = self.project_root / path
        if not target.exists():
            return f"Error: File '{path}' not found."
        if target.is_dir():
            return f"Error: '{path}' is a directory. Use a different tool for directories."
        try:
            os.remove(target)
            return f"Successfully deleted file '{path}'."
        except Exception as e:
            return f"Error deleting file: {e}"


class CreateDirTool(BaseTool):
    name = "create_dir"
    description = "Creates a new directory, including any necessary parent directories."
    args_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "The relative path of the directory to create."}
        },
        "required": ["path"]
    }

    def execute(self, path: str) -> str:
        target = self.project_root / path
        try:
            os.makedirs(target, exist_ok=True)
            return f"Successfully created directory '{path}'."
        except Exception as e:
            return f"Error creating directory: {e}"

