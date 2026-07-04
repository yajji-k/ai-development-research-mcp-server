import logging
from pathlib import Path
from typing import Callable, TypeVar

from app.config.settings import get_settings
from app.exceptions import ApplicationError
from app.schemas.filesystem import (
    CreateFileResponse,
    DeleteFileResponse,
    DirectoryEntry,
    EditFileResponse,
    ListDirectoryResponse,
    ReadFileResponse,
)

from .workspace_service import WorkspaceService

logger = logging.getLogger(__name__)
T = TypeVar("T")


class FileService:
    def __init__(self, workspace_root: Path | None = None) -> None:
        settings = get_settings()
        self._workspace_service = WorkspaceService(
            workspace_root=workspace_root or settings.workspace_root,
        )

    def read_file(self, path: str, encoding: str = "utf-8") -> ReadFileResponse:
        """
        Read and return the contents of a file.
        """
        resolved = self._workspace_service.resolve_path(path)
        display_path = self._workspace_service.relative_display_path(resolved)
        self._workspace_service.ensure_file(resolved, display_path)

        content = self._run_operation(
            operation="read_file",
            path=display_path,
            action=lambda: resolved.read_text(encoding=encoding),
        )

        return ReadFileResponse(
            path=display_path,
            content=content,
        )

    def create_file(
        self,
        path: str,
        content: str = "",
        encoding: str = "utf-8",
    ) -> CreateFileResponse:
        """
        Create a new file and write the supplied content.

        Raises:
            ApplicationError: If the file already exists.
        """
        resolved = self._workspace_service.resolve_path(path)
        display_path = self._workspace_service.relative_display_path(resolved)

        if resolved.exists():
            raise ApplicationError(f"File already exists: {display_path}")

        def write_file() -> None:
            self._workspace_service.ensure_parent_exists(resolved)
            with resolved.open("x", encoding=encoding) as file:
                file.write(content)

        self._run_operation(
            operation="create_file",
            path=display_path,
            action=write_file,
        )

        return CreateFileResponse(
            path=display_path,
            message="File created successfully.",
        )

    def edit_file(
        self,
        path: str,
        content: str,
        encoding: str = "utf-8",
    ) -> EditFileResponse:
        """
        Replace the contents of an existing file.
        """
        resolved = self._workspace_service.resolve_path(path)
        display_path = self._workspace_service.relative_display_path(resolved)
        self._workspace_service.ensure_file(resolved, display_path)

        self._run_operation(
            operation="edit_file",
            path=display_path,
            action=lambda: resolved.write_text(content, encoding=encoding),
        )

        return EditFileResponse(
            path=display_path,
            message="File updated successfully.",
        )

    def delete_file(self, path: str) -> DeleteFileResponse:
        """
        Delete the specified file.
        """
        resolved = self._workspace_service.resolve_path(path)
        display_path = self._workspace_service.relative_display_path(resolved)
        self._workspace_service.ensure_file(resolved, display_path)

        self._run_operation(
            operation="delete_file",
            path=display_path,
            action=resolved.unlink,
        )

        return DeleteFileResponse(
            path=display_path,
            message="File deleted successfully.",
        )

    def list_directory(self, path: str = ".") -> ListDirectoryResponse:
        """
        List the contents of a directory.
        """
        resolved = self._workspace_service.resolve_path(path)
        display_path = self._workspace_service.relative_display_path(resolved)
        self._workspace_service.ensure_directory(resolved, display_path)

        entries = self._run_operation(
            operation="list_directory",
            path=display_path,
            action=lambda: self._build_directory_entries(resolved),
        )

        return ListDirectoryResponse(
            path=display_path,
            entries=entries,
        )

    def _build_directory_entries(self, directory: Path) -> list[DirectoryEntry]:
        entries = []
        for item in directory.iterdir():
            is_file = item.is_file()
            entries.append(
                DirectoryEntry(
                    name=item.name,
                    is_file=is_file,
                    is_directory=item.is_dir(),
                    size=item.stat().st_size if is_file else None,
                ),
            )

        return sorted(entries, key=lambda entry: entry.name)

    def _run_operation(
        self,
        operation: str,
        path: str,
        action: Callable[[], T],
    ) -> T:
        logger.info("Filesystem operation '%s' started for path '%s'", operation, path)

        try:
            result = action()
        except UnicodeError as exc:
            logger.warning(
                "Filesystem operation '%s' failed for path '%s'",
                operation,
                path,
                exc_info=True,
            )
            raise ApplicationError(f"Unable to decode file: {path}") from exc
        except OSError as exc:
            logger.warning(
                "Filesystem operation '%s' failed for path '%s'",
                operation,
                path,
                exc_info=True,
            )
            raise ApplicationError(
                f"Filesystem operation failed for path: {path}"
            ) from exc

        logger.info(
            "Filesystem operation '%s' completed for path '%s'",
            operation,
            path,
        )
        return result
