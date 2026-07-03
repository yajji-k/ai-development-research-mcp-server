from .server_info_resource import server_info
from .health_resource import health
from .capability_resource import capability
from .register import register_resources

__all__ = [
    "server_info",
    "health",
    "capability",
    "register_resources"
]
