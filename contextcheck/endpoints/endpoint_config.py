from pydantic import BaseModel, ConfigDict


class EndpointConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    kind: str = "openai"
    url: str = ""  # AnyUrl type can be applied
    model: str | None = "gpt-3.5-turbo"
    additional_headers: dict = {}
