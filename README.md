# Production MCP Server - A secure, observable AI infrastructure service for exposing tools, resources, and prompts to MCP-compatible clients.

A production-oriented **Model Context Protocol (MCP)** server built with **FastMCP**, **FastAPI**, and **Pydantic Settings**. This project demonstrates the engineering patterns behind reliable AI tool infrastructure: clean architecture, typed contracts, dual transport support, HTTP authentication, runtime telemetry, Dockerized deployment, and an extensible capability registry.

## About

This server is designed as a compact but production-minded MCP runtime for AI agents and developer tooling. It exposes utility, filesystem, Git, metadata, and prompt capabilities through a modular Python codebase that separates protocol adapters from business logic.

For AI engineering and infrastructure work, the project highlights several important practices:

- Designing tool servers that work for both local agent workflows and networked deployments.
- Keeping MCP adapters thin while placing testable behavior in service classes.
- Using typed Pydantic schemas for predictable tool, resource, and prompt responses.
- Centralizing capability registration so new tools can be added without scattering server setup logic.
- Capturing execution telemetry and audit events across tools, resources, and prompts.
- Protecting HTTP deployments with bearer-token API key authentication.
- Packaging the runtime for repeatable local, CI, and containerized execution.

## Features

| Area | Highlights |
| --- | --- |
| MCP runtime | FastMCP-based server with modular registration for tools, resources, and prompts. |
| Dual transport | STDIO for local MCP clients and HTTP transport through FastAPI/Uvicorn. |
| Security | Bearer-token API key middleware for authenticated HTTP access. |
| Observability | Telemetry decorators record execution status, duration, and audit events. |
| Typed configuration | Environment-driven settings via Pydantic Settings and optional `.env` files. |
| Workspace tooling | Filesystem tools operate inside a configured workspace boundary. |
| Git tooling | Structured Git status, diff, branch, and log capabilities for development agents. |
| Prompt engineering | Reusable development prompts for code review, bug reporting, and API docs. |
| Quality | Unit tests cover services, adapters, registries, telemetry, resources, prompts, and server creation. |
| Deployment | Dockerfile included for containerized execution. |

## Tech Stack

- **Python 3.13**
- **FastMCP** for MCP server functionality
- **FastAPI** for HTTP hosting
- **Uvicorn** as the ASGI server
- **Pydantic Settings** for environment-based configuration
- **Pytest** for tests
- **Ruff** for linting
- **uv** for dependency management
- **Docker** for containerized execution

## Project Structure

```text
app/
  api/                 FastAPI application factory and HTTP mounting
  auth/                API key middleware
  config/              Runtime settings and transport configuration
  exceptions/          Application-specific exception types
  prompts/             MCP prompt adapters
  registry/            Central registration for tools, resources, and prompts
  resources/           MCP resource adapters
  schemas/             Typed response schemas
  server/              MCP server factory and bootstrap entrypoint
  services/            Business logic for tools, resources, prompts, Git, and files
  telemetry/           Logging, audit events, and execution decorators
  tools/               MCP tool adapters
tests/
  unit/                Unit tests grouped by layer and capability
Dockerfile             Container image definition
pyproject.toml         Project metadata, dependencies, and test config
uv.lock                Locked dependency graph
```

## Available Capabilities

### Tools

| Category | Tool | Description |
| --- | --- | --- |
| Utility | `ping` | Returns a basic health response confirming the server is running. |
| Utility | `echo` | Returns the provided message after validating that it is not empty. |
| Utility | `uuid` | Generates a UUID v4 value. |
| Filesystem | `read_file` | Reads a file inside the configured workspace. |
| Filesystem | `create_file` | Creates a new workspace file with optional initial content. |
| Filesystem | `edit_file` | Replaces the contents of an existing workspace file. |
| Filesystem | `delete_file` | Deletes a file inside the configured workspace. |
| Filesystem | `list_directory` | Lists directory entries with file/directory metadata. |
| Git | `git_status` | Returns short Git status with branch information. |
| Git | `git_diff` | Returns staged or unstaged Git diff output. |
| Git | `git_log` | Returns recent commits as structured log entries. |
| Git | `git_branch` | Returns the current branch and local branch list. |

### Resources

| Resource URI | Description |
| --- | --- |
| `server://info` | Returns server name, version, Python version, log level, and transport metadata. |
| `server://health` | Returns the current server health status. |
| `server://capabilities` | Returns registered server capabilities. |

### Prompts

| Prompt | Description |
| --- | --- |
| `code_review` | Builds a structured senior-engineer code review prompt for a selected language. |
| `bug_report` | Builds a QA-focused bug report prompt for a selected project. |
| `api_documentation` | Builds a technical-writing prompt for documenting APIs in a selected framework. |

## Configuration

Settings are loaded from environment variables or a local `.env` file.

| Variable | Default | Description |
| --- | --- | --- |
| `SERVER_NAME` | `MCP Server` | Display name used by the MCP server. |
| `SERVER_VERSION` | `0.1.0` | Server version exposed through metadata. |
| `LOG_LEVEL` | `INFO` | Logging level. |
| `TRANSPORT` | `stdio` | Runtime transport. Supported values: `stdio`, `http`. |
| `HTTP_HOST` | `0.0.0.0` | Host used by the HTTP server. |
| `HTTP_PORT` | `8000` | Port used by the HTTP server. |
| `API_KEY` | `change-me` | Bearer token required for authenticated HTTP requests. |
| `WORKSPACE_ROOT` | Current working directory | Root directory used by filesystem and Git tools. |

Example `.env`:

```env
SERVER_NAME="MCP Server"
SERVER_VERSION="0.1.0"
LOG_LEVEL="INFO"
TRANSPORT="http"
HTTP_HOST="0.0.0.0"
HTTP_PORT=8000
API_KEY="replace-with-a-secret"
WORKSPACE_ROOT="/path/to/workspace"
```

## Getting Started

### 1. Install dependencies

```bash
uv sync
```

### 2. Run with STDIO transport

STDIO is the default transport and is useful when connecting the server directly to an MCP-compatible local client.

```bash
uv run python -m app.server.bootstrap
```

### 3. Run with HTTP transport

Set the transport to HTTP and start the server:

```bash
TRANSPORT=http API_KEY=replace-with-a-secret uv run python -m app.server.bootstrap
```

The MCP app is mounted under:

```text
http://localhost:8000/mcp-server/mcp
```

HTTP requests must include the configured bearer token:

```http
Authorization: Bearer replace-with-a-secret
```

### 4. Run with auto-reload during development

```bash
TRANSPORT=http API_KEY=replace-with-a-secret uv run python -m app.server.bootstrap --reload
```

## Docker

Build the image:

```bash
docker build -t mcp-server .
```

Run with STDIO defaults:

```bash
docker run --rm mcp-server
```

Run with HTTP transport:

```bash
docker run --rm -p 8000:8000 \
  -e TRANSPORT=http \
  -e API_KEY=replace-with-a-secret \
  mcp-server
```

## Testing and Quality

Run the test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

The tests cover the main layers of the application, including service behavior, MCP adapters, prompt generation, resource registration, telemetry, Git operations, filesystem operations, and server creation.

## Architecture Notes

The server is intentionally split into adapters and services. MCP-facing functions in `app/tools`, `app/resources`, and `app/prompts` stay thin, while application logic lives in `app/services`. This keeps each capability easy to test without booting the full MCP runtime.

The registration layer in `app/registry` keeps server assembly centralized. `create_server()` builds the FastMCP instance and registers every tool, resource, and prompt in one place. For HTTP mode, `create_app()` wraps the MCP HTTP app with FastAPI middleware and mounts it under `/mcp-server`.

Filesystem and Git capabilities are scoped through the configured `WORKSPACE_ROOT`, giving AI agents practical development tools while keeping path handling explicit and testable. Filesystem paths are resolved against the workspace boundary before operations are executed.

Telemetry is implemented with decorators around tools, resources, and prompts. Each execution records success or failure, duration in milliseconds, and audit events in `logs/audit.log` at runtime.

## Extending the Server

To add a new tool:

1. Create a service method under `app/services`.
2. Define any request or response schemas under `app/schemas`.
3. Add a thin MCP adapter under `app/tools`.
4. Register the adapter in the relevant registration module, such as `app/tools/utility/register.py`, or create a new capability module.
5. Add focused unit tests for the service and adapter.

The same pattern applies to resources and prompts: keep framework-facing adapters small, place logic in services, register capabilities centrally, and add tests close to the behavior being introduced.

## Future Enhancements

- Add more AI engineering tools for retrieval workflows, model evaluation, dataset inspection, and prompt/version management.
- Expand Git automation with commit summaries, PR readiness checks, and repository health diagnostics.
- Add richer observability options such as structured JSON logs, metrics export, and distributed tracing hooks.
- Introduce role-based authorization and per-tool access policies for multi-user HTTP deployments.
