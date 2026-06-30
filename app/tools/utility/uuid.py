from app.services.utility import UUIDService

service = UUIDService()

def generate_uuid():
    """Generate a new UUID version 4."""
    return service.get_uuid()