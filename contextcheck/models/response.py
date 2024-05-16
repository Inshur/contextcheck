from pydantic import BaseModel


class ResponseStats(BaseModel):
    tokens_request: int | None = None
    tokens_response: int | None = None
    tokens_total: int | None = None


class ResponseBase(BaseModel):
    message: str | None
    _stats: ResponseStats = ResponseStats()
