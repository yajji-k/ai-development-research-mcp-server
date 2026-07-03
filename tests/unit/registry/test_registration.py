from app.prompts.development import api_documentation, bug_report, code_review
from app.prompts.development import register as development_prompt_register
from app.registry import prompt_registry, resource_registry, tool_registry
from app.resources.utility import capability, health, server_info
from app.resources.utility import register as utility_resource_register
from app.tools.utility import echo, ping, uuid
from app.tools.utility import register as utility_tool_register


class FakeServer:
    def __init__(self) -> None:
        self.prompts = []
        self.resources = []
        self.tools = []

    def prompt(self, *, name: str, description: str):
        def decorator(handler):
            self.prompts.append(
                {
                    "description": description,
                    "handler": handler,
                    "name": name,
                },
            )
            return handler

        return decorator

    def resource(self, uri: str):
        def decorator(handler):
            self.resources.append((uri, handler))
            return handler

        return decorator

    def tool(self):
        def decorator(handler):
            self.tools.append(handler)
            return handler

        return decorator


def test_utility_tool_package_registers_utility_tools() -> None:
    server = FakeServer()

    utility_tool_register.register_tools(server)

    assert server.tools == [
        ping,
        echo,
        uuid,
    ]


def test_utility_resource_package_registers_utility_resources() -> None:
    server = FakeServer()

    utility_resource_register.register_resources(server)

    assert server.resources == [
        ("server://info", server_info),
        ("server://health", health),
        ("server://capabilities", capability),
    ]


def test_development_prompt_package_registers_development_prompts() -> None:
    server = FakeServer()

    development_prompt_register.register_prompts(server)

    assert server.prompts == [
        {
            "description": "Generate a prompt for reviewing source code.",
            "handler": code_review,
            "name": "code_review",
        },
        {
            "description": "Generate a prompt for creating bug reports.",
            "handler": bug_report,
            "name": "bug_report",
        },
        {
            "description": "Generate a prompt for creating API documentation.",
            "handler": api_documentation,
            "name": "api_documentation",
        },
    ]


def test_tool_registry_delegates_to_package_registrars(monkeypatch) -> None:
    calls = []
    server = object()

    def register_first(received_server) -> None:
        calls.append(("first", received_server))

    def register_second(received_server) -> None:
        calls.append(("second", received_server))

    monkeypatch.setattr(
        tool_registry,
        "TOOL_REGISTRARS",
        (register_first, register_second),
    )

    tool_registry.register_tools(server)

    assert calls == [
        ("first", server),
        ("second", server),
    ]


def test_resource_registry_delegates_to_package_registrars(monkeypatch) -> None:
    calls = []
    server = object()

    def register_first(received_server) -> None:
        calls.append(("first", received_server))

    def register_second(received_server) -> None:
        calls.append(("second", received_server))

    monkeypatch.setattr(
        resource_registry,
        "RESOURCE_REGISTRARS",
        (register_first, register_second),
    )

    resource_registry.register_resources(server)

    assert calls == [
        ("first", server),
        ("second", server),
    ]


def test_prompt_registry_delegates_to_package_registrars(monkeypatch) -> None:
    calls = []
    server = object()

    def register_first(received_server) -> None:
        calls.append(("first", received_server))

    def register_second(received_server) -> None:
        calls.append(("second", received_server))

    monkeypatch.setattr(
        prompt_registry,
        "PROMPT_REGISTRARS",
        (register_first, register_second),
    )

    prompt_registry.register_prompts(server)

    assert calls == [
        ("first", server),
        ("second", server),
    ]
