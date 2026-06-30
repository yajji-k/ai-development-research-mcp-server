from app.services.utility.server_info_service import ServerInfoService

service = ServerInfoService()


def server_info():
    """MCP tool for getting server_info"""
    return service.get_server_info()