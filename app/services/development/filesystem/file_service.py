from pathlib import Path

from app.exceptions import ApplicationError
from app.schemas.filesystem import DirectoryEntry

from .workspace_service import WorkspaceService


class FileService:
    def __init__(self, workspace_root: Path | None = None) -> None:
        self._workspace_service = WorkspaceService(
            workspace_root=workspace_root or Path.cwd(),
        )

    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        """
        Read and return the contents of a file.
        """
        resolved = self._workspace_service.resolve_path(path)
        self._workspace_service.ensure_file(resolved)

        return resolved.read_text(encoding=encoding)

    def create_file(
        self,
        path: str,
        content: str = "",
        encoding: str = "utf-8",
    ) -> None:
        """
        Create a new file and write the supplied content.

        Raises:
            ApplicationError: If the file already exists.
        """
        resolved = self._workspace_service.resolve_path(path)

        if resolved.exists():
            raise ApplicationError(f"File already exists: {path}")

        self._workspace_service.ensure_parent_exists(resolved)

        resolved.write_text(content, encoding=encoding)

    def edit_file(
        self,
        path: str,
        content: str,
        encoding: str = "utf-8",
    ) -> None:
        """
        Replace the contents of an existing file.
        """
        resolved = self._workspace_service.resolve_path(path)
        self._workspace_service.ensure_file(resolved)

        resolved.write_text(content, encoding=encoding)

    def delete_file(self, path: str) -> None:
        """
        Delete the specified file.
        """
        resolved = self._workspace_service.resolve_path(path)
        self._workspace_service.ensure_file(resolved)

        resolved.unlink()

    def list_directory(self, path: str = ".") -> list[DirectoryEntry]:
        """
        List the contents of a directory.
        """
        resolved = self._workspace_service.resolve_path(path)
        self._workspace_service.ensure_directory(resolved)

        entries = []
        for item in resolved.iterdir():
            entries.append(
                DirectoryEntry(
                    name=item.name,
                    is_file=item.is_file(),
                    is_directory=item.is_dir(),
                    size=item.stat().st_size if item.is_file() else None,
                ),
            )

        return sorted(entries, key=lambda entry: entry.name)
