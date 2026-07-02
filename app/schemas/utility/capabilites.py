from pydantic import BaseModel

class CapabilitiesResponse(BaseModel):
    tools: list[str]
    resources: list[str]
    prompts: list[str]
    transports: list[str]