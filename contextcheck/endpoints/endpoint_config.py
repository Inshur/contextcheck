from pydantic import BaseModel, ConfigDict


# NOTE RB: Imo, we should think how to refactor this as not every endpoint need those params
# and some new endpoints/connectors might need other values
class EndpointConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    kind: str = "openai"
    url: str = ""  # AnyUrl type can be applied
    model: str | None = "gpt-4o-mini"
    additional_headers: dict = {}

    provider: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None

    top_k: int = 3
    use_ranker: bool = True
    collection_name: str = "default"
