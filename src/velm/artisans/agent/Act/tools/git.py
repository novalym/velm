# Path: artisans/agent/Act/tools/git.py
# -------------------------------------

import subprocess
import shlex
import re
from typing import Optional

from .base import BaseTool
from .....interfaces.requests import SemDiffRequest


class GitStatusTool(BaseTool):
    """The Gaze of the Present."""
    name: str = "git_status"
    description: str = "Perceives the current state of the working tree, showing new, modified, or staged files. Returns the output of `git status --porcelain`."
    args_schema: dict = {"type": "object", "properties": {}}

    def execute(self) -> str:
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root, text=True, check=True, capture_output=True
            )
            return result.stdout or "The working tree is pure. No changes detected."
        except subprocess.CalledProcessError as e:
            return f"Error perceiving Git status: {e.stderr}"
        except FileNotFoundError:
            return "Error: The 'git' artisan is not manifest in this reality."


class GitStageFileTool(BaseTool):
    """The Hand of Consecration."""
    name: str = "git_stage_file"
    description: str = "Consecrates a file's soul to the index, preparing it for commitment to the eternal chronicle. Use '.' to stage all changes."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The relative path to the file to stage. Use '.' to stage all."
            }
        },
        "required": ["path"]
    }

    def execute(self, path: str) -> str:
        try:
            subprocess.run(
                ["git", "add", path],
                cwd=self.project_root, check=True, capture_output=True
            )
            return f"Successfully staged '{path}'."
        except subprocess.CalledProcessError as e:
            return f"Error staging '{path}': {e.stderr}"


class GitDiffTool(BaseTool):
    """The Gaze of Divergence."""
    name: str = "git_diff"
    description: str = "Perceives the divergence between realities (e.g., working tree vs. index). Can show a full diff, or just the names of changed files."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Optional: The specific file to diff. If omitted, shows all changes."
            },
            "staged": {
                "type": "boolean",
                "description": "If true, shows the diff for staged changes (what will be committed). Defaults to false (working directory changes)."
            },
            "name_only": {
                "type": "boolean",
                "description": "If true, returns only the names of changed files, not their content. This is a fast way to get a summary."
            }
        },
        "required": []
    }

    def execute(self, file_path: Optional[str] = None, staged: bool = False, name_only: bool = False) -> str:
        try:
            cmd = ["git", "diff"]
            if staged:
                cmd.append("--staged")
            if name_only:
                cmd.append("--name-only")
            if file_path:
                cmd.append("--")
                cmd.append(file_path)

            result = subprocess.run(cmd, cwd=self.project_root, text=True, check=True, capture_output=True)
            return result.stdout or "No divergence perceived."
        except subprocess.CalledProcessError as e:
            return f"Error calculating diff: {e.stderr}"


class GitSemanticDiffTool(BaseTool):
    """The God-Tier Gaze."""
    name: str = "git_semantic_diff"
    description: str = "Performs a Gnostic, Abstract Syntax Tree (AST) comparison of a staged file against HEAD. It reveals *what* changed (functions, classes), not just which lines. This is the highest form of perception."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The relative path to the staged file to analyze."
            }
        },
        "required": ["file_path"]
    }

    def execute(self, file_path: str) -> str:
        # This is the Gnostic link. This tool summons another Scaffold Artisan.
        self.engine.logger.info(f"The Agent's Gaze turns inward, summoning the SemDiff Artisan for '{file_path}'...")
        req = SemDiffRequest(
            target=file_path,
            reference="HEAD"
        )
        result = self.engine.dispatch(req)
        if result.success:
            # Format the data into a string for the agent
            if result.data and 'changes' in result.data:
                summary = [f"Semantic changes for {file_path}:"]
                for change in result.data['changes']:
                    summary.append(
                        f"- {change['change_type']} {change['symbol_type']}: {change['symbol_name']} ({change['details']})")
                return "\n".join(summary)
            return f"No semantic changes detected for {file_path}."
        else:
            return f"Error performing semantic diff: {result.message}"


class GitCommitTool(BaseTool):
    """The Guardian of History."""
    name: str = "git_commit"
    description: str = "Inscribes the current state of the index into the eternal chronicle. The message MUST follow the Conventional Commit format (e.g., 'feat(scope): description')."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The commit message, strictly following Conventional Commit format."
            }
        },
        "required": ["message"]
    }

    def execute(self, message: str) -> str:
        # The Guardian's Gaze: Enforce Conventional Commit format
        pattern = r"^(feat|fix|docs|style|refactor|perf|test|chore|build|ci)(\(\w+\))?:\s.+"
        if not re.match(pattern, message):
            return f"Error: Commit message is profane. It MUST follow Conventional Commit format (e.g., 'feat(api): add new endpoint'). Your message was: '{message}'"

        try:
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_root, text=True, check=True, capture_output=True
            )
            return "Commit successfully inscribed into the chronicle."
        except subprocess.CalledProcessError as e:
            return f"Error during commit: {e.stderr}"


class GitLogSummaryTool(BaseTool):
    """The Temporal Telescope."""
    name: str = "git_log_summary"
    description: str = "Gazes into the past, returning a brief summary of the most recent commits on the current branch."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "The number of recent commits to show. Defaults to 5."
            }
        },
        "required": []
    }

    def execute(self, limit: int = 5) -> str:
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "--decorate", "-n", str(limit)],
                cwd=self.project_root, text=True, check=True, capture_output=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error reading git log: {e.stderr}"


class GitBranchTool(BaseTool):
    """The Weaver of Timelines."""
    name: str = "git_branch"
    description: str = "Creates a new branch (timeline) for isolated work. Does not switch to it."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "branch_name": {
                "type": "string",
                "description": "The name of the new branch to create."
            }
        },
        "required": ["branch_name"]
    }

    def execute(self, branch_name: str) -> str:
        try:
            subprocess.run(
                ["git", "branch", branch_name],
                cwd=self.project_root, text=True, check=True, capture_output=True
            )
            return f"New timeline '{branch_name}' has been forged."
        except subprocess.CalledProcessError as e:
            return f"Error forging branch: {e.stderr}"


class GitCheckoutTool(BaseTool):
    """The Time-Turner."""
    name: str = "git_checkout"
    description: str = "Switches the current reality to a different branch (timeline)."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "branch_name": {
                "type": "string",
                "description": "The name of the branch to switch to."
            }
        },
        "required": ["branch_name"]
    }

    def execute(self, branch_name: str) -> str:
        try:
            subprocess.run(
                ["git", "checkout", branch_name],
                cwd=self.project_root, text=True, check=True, capture_output=True
            )
            return f"Reality has been shifted to the '{branch_name}' timeline."
        except subprocess.CalledProcessError as e:
            return f"Error shifting timelines: {e.stderr}"


class GitListBranchesTool(BaseTool):
    """The Oracle of Timelines."""
    name: str = "git_list_branches"
    description: str = "Proclaims all known timelines (branches) in this reality."
    args_schema: dict = {"type": "object", "properties": {}}

    def execute(self) -> str:
        try:
            result = subprocess.run(
                ["git", "branch"],
                cwd=self.project_root, text=True, check=True, capture_output=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error perceiving timelines: {e.stderr}"

