# MCP Server

A production-oriented Model Context Protocol (MCP) server built with **FastMCP**, **FastAPI**, and **Pydantic Settings**. The project demonstrates how to expose tools, resources, and reusable prompts through a clean, testable Python architecture with support for both local STDIO usage and authenticated HTTP transport.

## Overview

This server provides a small but extensible MCP runtime that can be connected to MCP-compatible clients. It includes utility tools, server metadata resources, development-focused prompt templates, API key middleware for HTTP deployments, and execution telemetry for tools, resources, and prompts.

The codebase is organized around separation of concerns:

- **MCP adapters** register tools, resources, and prompts with FastMCP.
- **Service classes** contain business logic independently from transport details.
- **Pydantic schemas** define structured responses.
- **Registries** centralize capability registration.
- **Telemetry decorators** capture execution status and duration.
- **FastAPI integration** hosts the MCP app behind HTTP middleware.

## Features

- FastMCP server with modular registration for tools, resources, and prompts
- STDIO transport for local MCP client integration
- HTTP transport through FastAPI and Uvicorn
- Bearer-token API key authentication for HTTP requests
- CORS middleware configured for MCP HTTP headers
- Typed configuration through environment variables and `.env` files
- Structured utility tools:
  - `ping`
  - `echo`
  - `uuid`
- MCP resources:
  - `server://info`
  - `server://health`
  - `server://capabilities`
- Development prompt templates:
  - `code_review`
  - `bug_report`
  - `api_documentation`
- Audit logging for tool, resource, and prompt execution
- Unit test coverage for services, tools, resources, prompts, telemetry, registry behavior, and server creation
- Docker support for containerized execution

## Tech Stack

- **Python 3.13**
- **FastMCP** for MCP server functionality
- **FastAPI** for HTTP hosting
- **Uvicorn** as the ASGI server
- **Pydantic Settings** for environment-based configuration
- **Pytest** for tests
- **Ruff** for linting
- **uv** for dependency management

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
  services/            Business logic for tools, resources, and prompts
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

| Tool | Description |
| --- | --- |
| `ping` | Returns a basic health response confirming the server is running. |
| `echo` | Returns the provided message after validating that it is not empty. |
| `uuid` | Generates a UUID v4 value. |

### Resources

| Resource URI | Description |
| --- | --- |
| `server://info` | Returns server name, version, Python version, log level, and transport metadata. |
| `server://health` | Returns the current health status. |
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

Example `.env`:

```env
SERVER_NAME="MCP Server"
SERVER_VERSION="0.1.0"
LOG_LEVEL="INFO"
TRANSPORT="http"
HTTP_HOST="0.0.0.0"
HTTP_PORT=8000
API_KEY="replace-with-a-secret"
```

## Getting Started

### 1. Install dependencies

```bash
uv sync
```

### 2. Run with STDIO transport

STDIO is the default transport and is useful when connecting the server directly to an MCP-compatible client.

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

The tests cover the main layers of the application, including service behavior, MCP adapters, prompt generation, resource registration, telemetry, and server creation.

## Architecture Notes

The server is intentionally split into adapters and services. MCP-facing functions in `app/tools`, `app/resources`, and `app/prompts` stay thin, while the application logic lives in `app/services`. This makes each capability easier to test without needing to boot the full MCP runtime.

The registration layer in `app/registry` keeps server assembly centralized. `create_server()` builds the FastMCP instance and registers every tool, resource, and prompt in one place. For HTTP mode, `create_app()` wraps the MCP HTTP app with FastAPI middleware and mounts it under `/mcp-server`.

Telemetry is implemented with decorators around tools, resources, and prompts. Each execution records success or failure, duration in milliseconds, and audit events in `logs/audit.log` at runtime.

## Extending the Server

To add a new tool:

1. Create a service method under `app/services`.
2. Define any request or response schemas under `app/schemas`.
3. Add a thin MCP adapter under `app/tools`.
4. Register the adapter in `app/tools/utility/register.py` or a new registration module.
5. Add focused unit tests for the service and adapter.

The same pattern applies to resources and prompts: keep framework-facing adapters small, place logic in services, register capabilities centrally, and add tests close to the behavior being introduced.
