from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired

import pytest

from app.exceptions import ApplicationError
from app.schemas.git import (
    GitBranchResponse,
    GitDiffResponse,
    GitLogResponse,
    GitStatusResponse,
)
from app.services.git import GitService


def test_git_status_runs_short_branch_status(monkeypatch, tmp_path: Path) -> None:
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))
        return CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="## main\n M app.py\n",
            stderr="",
        )

    monkeypatch.setattr("app.services.git.git_service.subprocess.run", fake_run)
    service = GitService(workspace_root=tmp_path)

    response = service.git_status()

    assert isinstance(response, GitStatusResponse)
    assert response.output == "## main\n M app.py"
    assert response.lines == ["## main", " M app.py"]
    assert calls[0][0][0] == ["git", "status", "--short", "--branch"]
    assert calls[0][1]["cwd"] == tmp_path.resolve()
    assert calls[0][1]["shell"] is False
    assert calls[0][1]["timeout"] == 10


def test_git_diff_supports_staged(monkeypatch, tmp_path: Path) -> None:
    calls = []

    def fake_run(*args, **kwargs):
        calls.append(args[0])
        return CompletedProcess(args=args[0], returncode=0, stdout="diff", stderr="")

    monkeypatch.setattr("app.services.git.git_service.subprocess.run", fake_run)
    service = GitService(workspace_root=tmp_path)

    response = service.git_diff(staged=True)

    assert isinstance(response, GitDiffResponse)
    assert response.staged is True
    assert response.diff == "diff"
    assert calls == [["git", "diff", "--cached"]]


def test_git_log_returns_structured_commits(monkeypatch, tmp_path: Path) -> None:
    stdout = (
        "abc123\x1fabc\x1fAda\x1fada@example.com\x1f2026-01-01T00:00:00+00:00\x1fInit"
    )

    def fake_run(*args, **kwargs):
        return CompletedProcess(args=args[0], returncode=0, stdout=stdout, stderr="")

    monkeypatch.setattr("app.services.git.git_service.subprocess.run", fake_run)
    service = GitService(workspace_root=tmp_path)

    response = service.git_log(limit=1)

    assert isinstance(response, GitLogResponse)
    assert len(response.commits) == 1
    assert response.commits[0].commit_hash == "abc123"
    assert response.commits[0].short_hash == "abc"
    assert response.commits[0].author_name == "Ada"
    assert response.commits[0].author_email == "ada@example.com"
    assert response.commits[0].subject == "Init"


def test_git_log_rejects_invalid_limit(tmp_path: Path) -> None:
    service = GitService(workspace_root=tmp_path)

    with pytest.raises(ApplicationError, match="limit must be greater than 0"):
        service.git_log(limit=0)


def test_git_branch_returns_current_and_branches(monkeypatch, tmp_path: Path) -> None:
    def fake_run(*args, **kwargs):
        return CompletedProcess(
            args=args[0],
            returncode=0,
            stdout="  develop\n* main\n",
            stderr="",
        )

    monkeypatch.setattr("app.services.git.git_service.subprocess.run", fake_run)
    service = GitService(workspace_root=tmp_path)

    response = service.git_branch()

    assert isinstance(response, GitBranchResponse)
    assert response.current_branch == "main"
    assert [branch.name for branch in response.branches] == ["develop", "main"]
    assert [branch.is_current for branch in response.branches] == [False, True]


def test_git_command_failure_is_application_error(monkeypatch, tmp_path: Path) -> None:
    def fake_run(*args, **kwargs):
        return CompletedProcess(
            args=args[0],
            returncode=128,
            stdout="",
            stderr="not a git repository",
        )

    monkeypatch.setattr("app.services.git.git_service.subprocess.run", fake_run)
    service = GitService(workspace_root=tmp_path)

    with pytest.raises(ApplicationError, match="not a git repository"):
        service.git_status()


def test_git_timeout_is_application_error(monkeypatch, tmp_path: Path) -> None:
    def fake_run(*args, **kwargs):
        raise TimeoutExpired(cmd=args[0], timeout=10)

    monkeypatch.setattr("app.services.git.git_service.subprocess.run", fake_run)
    service = GitService(workspace_root=tmp_path)

    with pytest.raises(ApplicationError, match="timed out"):
        service.git_status()
