from pydantic import BaseModel


class GitStatusResponse(BaseModel):
    output: str
    lines: list[str]


class GitDiffResponse(BaseModel):
    staged: bool
    diff: str


class GitLogEntry(BaseModel):
    commit_hash: str
    short_hash: str
    author_name: str
    author_email: str
    date: str
    subject: str


class GitLogResponse(BaseModel):
    commits: list[GitLogEntry]


class GitBranch(BaseModel):
    name: str
    is_current: bool


class GitBranchResponse(BaseModel):
    current_branch: str
    branches: list[GitBranch]
