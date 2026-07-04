from pathlib import Path

from app.exceptions import ApplicationError


class WorkspaceService:
    def __init__(self, workspace_root: Path) -> None:
        self._workspace_root = workspace_root.resolve()

    def resolve_path(self, path: str) -> Path:
        """
        Resolve a user supplied path relative to the configured workspace.

        Raises:
            ApplicationError: If the resolved path escapes the workspace.
        """
        candidate = Path(path)

        if candidate.is_absolute():
            resolved = candidate.resolve()
        else:
            resolved = (self._workspace_root / candidate).resolve()

        if not self.is_within_workspace(resolved):
            raise ApplicationError(
                f"Path {path} is outside the configured workspace"
            )

        return resolved

    def ensure_exists(self, path: Path, display_path: str) -> None:
        """
        Ensure the supplied path exists.
        """
        if not path.exists():
            raise ApplicationError(f"Path does not exist: {display_path}")

    def ensure_directory(self, path: Path, display_path: str) -> None:
        self.ensure_exists(path, display_path)

        if not path.is_dir():
            raise ApplicationError(f"Path is not a directory: {display_path}")

    def ensure_file(self, path: Path, display_path: str) -> None:
        self.ensure_exists(path, display_path)

        if not path.is_file():
            raise ApplicationError(f"Path is not a file: {display_path}")

    def ensure_parent_exists(self, path: Path) -> None:
        """
        Ensure the parent directory exists.

        Missing parent directories are created automatically.
        """
        path.parent.mkdir(parents=True, exist_ok=True)

    def relative_display_path(self, path: Path) -> str:
        """
        Return a workspace-relative path for user-facing messages.
        """
        try:
            return str(path.resolve().relative_to(self._workspace_root))
        except ValueError:
            return path.name

    def is_within_workspace(self, path: Path) -> bool:
        """
        Check whether the resolved path is inside the configured workspace.
        """
        try:
            path.resolve().relative_to(self._workspace_root)
            return True
        except ValueError:
            return False
