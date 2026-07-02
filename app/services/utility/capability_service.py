from app.schemas.utility import CapabilitiesResponse

class CapabilitiesService:
    
    def get_capability(self)->CapabilitiesResponse:
        return CapabilitiesResponse(
                    tools=[
                        "ping",
                        "echo",
                        "uuid",
                    ],
                    resources=[
                        "server://info",
                        "server://health",
                        "server://capabilities",
                    ],
                    prompts=[],
                    transports=[
                        "stdio",
                    ],
                )    
