from typing import Self

from pydantic import BaseModel

from contextcheck.models.models import TestStep


class MessageBase(BaseModel):

    @classmethod
    def from_test_step(cls, test_step: TestStep) -> Self:
        raise NotImplementedError("This method should be implemented!")


class ResponseStats(BaseModel):
    tokens_message: int | None = None
    tokens_response: int | None = None
    tokens_total: int | None = None


class ResponseBase(BaseModel):
    message: str | None
    stats: ResponseStats = ResponseStats()
