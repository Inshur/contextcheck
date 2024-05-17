from pydantic import BaseModel, ConfigDict


class ResponseStats(BaseModel):
    tokens_request: int | None = None
    tokens_response: int | None = None
    tokens_total: int | None = None


class ResponseBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    message: str | None = None
    _stats: ResponseStats = ResponseStats()
