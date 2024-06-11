from pydantic import BaseModel, ConfigDict


class ResponseStats(BaseModel):
    model_config = ConfigDict(extra="allow")
    tokens_request: int | None = None
    tokens_response: int | None = None
    tokens_total: int | None = None


class ResponseBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    message: str | None = None
    stats: ResponseStats = ResponseStats()
