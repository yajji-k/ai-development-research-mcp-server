from unittest.mock import Mock

import app.tools.filesystem.create_file_tool as create_file_tool
import app.tools.filesystem.delete_file_tool as delete_file_tool
import app.tools.filesystem.edit_file_tool as edit_file_tool
import app.tools.filesystem.list_directory_tool as list_directory_tool
import app.tools.filesystem.read_file_tool as read_file_tool


def test_read_file_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.read_file.return_value = expected_response
    monkeypatch.setattr(read_file_tool, "service", service)

    response = read_file_tool.read_file("README.md")

    service.read_file.assert_called_once_with("README.md")
    assert response is expected_response


def test_create_file_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.create_file.return_value = expected_response
    monkeypatch.setattr(create_file_tool, "service", service)

    response = create_file_tool.create_file("notes.txt", "hello")

    service.create_file.assert_called_once_with(path="notes.txt", content="hello")
    assert response is expected_response


def test_edit_file_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.edit_file.return_value = expected_response
    monkeypatch.setattr(edit_file_tool, "service", service)

    response = edit_file_tool.edit_file("notes.txt", "updated")

    service.edit_file.assert_called_once_with(path="notes.txt", content="updated")
    assert response is expected_response


def test_delete_file_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.delete_file.return_value = expected_response
    monkeypatch.setattr(delete_file_tool, "service", service)

    response = delete_file_tool.delete_file("notes.txt")

    service.delete_file.assert_called_once_with("notes.txt")
    assert response is expected_response


def test_list_directory_tool_calls_service_and_returns_response_unchanged(
    monkeypatch,
):
    service = Mock()
    expected_response = object()
    service.list_directory.return_value = expected_response
    monkeypatch.setattr(list_directory_tool, "service", service)

    response = list_directory_tool.list_directory("src")

    service.list_directory.assert_called_once_with("src")
    assert response is expected_response
