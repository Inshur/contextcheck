from pydantic import BaseModel


class ResponseStats(BaseModel):
    tokens_message: int | None = None
    tokens_response: int | None = None
    tokens_total: int | None = None


class ResponseBase(BaseModel):
    message: str | None
    stats: ResponseStats = ResponseStats()
