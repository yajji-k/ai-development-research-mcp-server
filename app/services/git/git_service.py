import logging
import subprocess
from pathlib import Path

from app.config.settings import get_settings
from app.exceptions import ApplicationError
from app.schemas.git import (
    GitBranch,
    GitBranchResponse,
    GitDiffResponse,
    GitLogEntry,
    GitLogResponse,
    GitStatusResponse,
)
from app.services.development.filesystem import WorkspaceService

logger = logging.getLogger(__name__)


class GitService:
    def __init__(self, workspace_root: Path | None = None) -> None:
        settings = get_settings()
        self._workspace_service = WorkspaceService(
            workspace_root=workspace_root or settings.workspace_root,
        )
        self._workspace_root = self._workspace_service.resolve_path(".")
        self._timeout_seconds = 10

    def git_status(self) -> GitStatusResponse:
        """
        Return short Git status with branch information.
        """
        output = self._run_git_command(
            operation="git_status",
            command=["git", "status", "--short", "--branch"],
        )

        return GitStatusResponse(
            output=output,
            lines=self._split_lines(output),
        )

    def git_diff(self, staged: bool = False) -> GitDiffResponse:
        """
        Return the Git diff for unstaged or staged changes.
        """
        command = ["git", "diff", "--cached"] if staged else ["git", "diff"]
        output = self._run_git_command(
            operation="git_diff",
            command=command,
        )

        return GitDiffResponse(
            staged=staged,
            diff=output,
        )

    def git_log(self, limit: int = 10) -> GitLogResponse:
        """
        Return recent Git commits as structured entries.
        """
        if limit < 1:
            raise ApplicationError("Git log limit must be greater than 0")

        output = self._run_git_command(
            operation="git_log",
            command=[
                "git",
                "log",
                "-n",
                str(limit),
                "--pretty=format:%H%x1f%h%x1f%an%x1f%ae%x1f%ad%x1f%s",
                "--date=iso-strict",
            ],
        )

        return GitLogResponse(
            commits=self._parse_log_entries(output),
        )

    def git_branch(self) -> GitBranchResponse:
        """
        Return the current branch and local branch list.
        """
        output = self._run_git_command(
            operation="git_branch",
            command=["git", "branch", "--list"],
        )
        branches = self._parse_branches(output)
        current_branch = next(
            (branch.name for branch in branches if branch.is_current),
            "",
        )

        return GitBranchResponse(
            current_branch=current_branch,
            branches=branches,
        )

    def _run_git_command(self, operation: str, command: list[str]) -> str:
        logger.info("Git operation '%s' started", operation)

        try:
            result = subprocess.run(
                command,
                cwd=self._workspace_root,
                capture_output=True,
                check=False,
                shell=False,
                text=True,
                timeout=self._timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            logger.warning("Git operation '%s' timed out", operation, exc_info=True)
            raise ApplicationError(f"Git operation timed out: {operation}") from exc
        except OSError as exc:
            logger.warning("Git operation '%s' failed", operation, exc_info=True)
            raise ApplicationError(f"Git operation failed: {operation}") from exc

        if result.returncode != 0:
            logger.warning(
                "Git operation '%s' failed with exit code %s",
                operation,
                result.returncode,
            )
            message = result.stderr.strip() or result.stdout.strip()
            raise ApplicationError(message or f"Git operation failed: {operation}")

        logger.info("Git operation '%s' completed", operation)
        return result.stdout.strip()

    def _parse_log_entries(self, output: str) -> list[GitLogEntry]:
        entries = []
        for line in self._split_lines(output):
            parts = line.split("\x1f", maxsplit=5)
            if len(parts) != 6:
                continue

            commit_hash, short_hash, author_name, author_email, date, subject = parts
            entries.append(
                GitLogEntry(
                    commit_hash=commit_hash,
                    short_hash=short_hash,
                    author_name=author_name,
                    author_email=author_email,
                    date=date,
                    subject=subject,
                ),
            )

        return entries

    def _parse_branches(self, output: str) -> list[GitBranch]:
        branches = []
        for line in self._split_lines(output):
            is_current = line.startswith("*")
            name = line[2:].strip() if is_current else line.strip()
            branches.append(
                GitBranch(
                    name=name,
                    is_current=is_current,
                ),
            )

        return branches

    def _split_lines(self, output: str) -> list[str]:
        return [line for line in output.splitlines() if line]
