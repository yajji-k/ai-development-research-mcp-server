from unittest.mock import Mock

import pytest

from app.exceptions import ApplicationError
import app.tools.git.git_branch_tool as git_branch_tool
import app.tools.git.git_diff_tool as git_diff_tool
import app.tools.git.git_log_tool as git_log_tool
import app.tools.git.git_status_tool as git_status_tool


def test_git_status_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.git_status.return_value = expected_response
    monkeypatch.setattr(git_status_tool, "service", service)

    response = git_status_tool.git_status()

    service.git_status.assert_called_once_with()
    assert response is expected_response


def test_git_diff_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.git_diff.return_value = expected_response
    monkeypatch.setattr(git_diff_tool, "service", service)

    response = git_diff_tool.git_diff(staged=True)

    service.git_diff.assert_called_once_with(staged=True)
    assert response is expected_response


def test_git_log_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.git_log.return_value = expected_response
    monkeypatch.setattr(git_log_tool, "service", service)

    response = git_log_tool.git_log(limit=3)

    service.git_log.assert_called_once_with(limit=3)
    assert response is expected_response


def test_git_log_tool_rejects_invalid_limit(monkeypatch):
    service = Mock()
    monkeypatch.setattr(git_log_tool, "service", service)

    with pytest.raises(ApplicationError, match="limit must be greater than 0"):
        git_log_tool.git_log(limit=0)

    service.git_log.assert_not_called()


def test_git_branch_tool_calls_service_and_returns_response_unchanged(monkeypatch):
    service = Mock()
    expected_response = object()
    service.git_branch.return_value = expected_response
    monkeypatch.setattr(git_branch_tool, "service", service)

    response = git_branch_tool.git_branch()

    service.git_branch.assert_called_once_with()
    assert response is expected_response
