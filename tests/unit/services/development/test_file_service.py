from pathlib import Path

import pytest

from app.exceptions import ApplicationError
from app.schemas.filesystem import (
    CreateFileResponse,
    DeleteFileResponse,
    EditFileResponse,
    ListDirectoryResponse,
    ReadFileResponse,
)
from app.services.development import FileService


def test_create_file_writes_content_inside_workspace(tmp_path: Path) -> None:
    service = FileService(workspace_root=tmp_path)

    response = service.create_file("notes/todo.txt", "ship it")

    assert isinstance(response, CreateFileResponse)
    assert response.path == "notes/todo.txt"
    assert (tmp_path / "notes" / "todo.txt").read_text() == "ship it"


def test_read_file_returns_response_model(tmp_path: Path) -> None:
    path = tmp_path / "hello.txt"
    path.write_text("Hello MCP")
    service = FileService(workspace_root=tmp_path)

    response = service.read_file("hello.txt")

    assert isinstance(response, ReadFileResponse)
    assert response.path == "hello.txt"
    assert response.content == "Hello MCP"


def test_edit_file_replaces_existing_content(tmp_path: Path) -> None:
    path = tmp_path / "hello.txt"
    path.write_text("old")
    service = FileService(workspace_root=tmp_path)

    response = service.edit_file("hello.txt", "new")

    assert isinstance(response, EditFileResponse)
    assert response.path == "hello.txt"
    assert path.read_text() == "new"


def test_delete_file_removes_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "hello.txt"
    path.write_text("bye")
    service = FileService(workspace_root=tmp_path)

    response = service.delete_file("hello.txt")

    assert isinstance(response, DeleteFileResponse)
    assert response.path == "hello.txt"
    assert not path.exists()


def test_list_directory_returns_sorted_metadata(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("two")
    (tmp_path / "a").mkdir()
    service = FileService(workspace_root=tmp_path)

    response = service.list_directory(".")

    assert isinstance(response, ListDirectoryResponse)
    assert response.path == "."
    assert [entry.name for entry in response.entries] == ["a", "b.txt"]
    assert response.entries[0].is_directory is True
    assert response.entries[0].is_file is False
    assert response.entries[0].size is None
    assert response.entries[1].is_file is True
    assert response.entries[1].size == 3


def test_path_traversal_outside_workspace_is_rejected(tmp_path: Path) -> None:
    service = FileService(workspace_root=tmp_path)

    with pytest.raises(ApplicationError, match="outside the configured workspace"):
        service.read_file("../outside.txt")


def test_missing_file_error_does_not_leak_absolute_path(tmp_path: Path) -> None:
    service = FileService(workspace_root=tmp_path)

    with pytest.raises(ApplicationError) as exc_info:
        service.read_file("missing.txt")

    message = str(exc_info.value)
    assert "missing.txt" in message
    assert str(tmp_path) not in message


def test_invalid_encoding_is_translated_to_application_error(
    tmp_path: Path,
) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff")
    service = FileService(workspace_root=tmp_path)

    with pytest.raises(ApplicationError, match="Unable to decode file: binary.txt"):
        service.read_file("binary.txt")


def test_symlink_escape_is_rejected(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-target.txt"
    outside.write_text("secret")
    link = tmp_path / "link.txt"
    link.symlink_to(outside)
    service = FileService(workspace_root=tmp_path)

    with pytest.raises(ApplicationError, match="outside the configured workspace"):
        service.read_file("link.txt")
