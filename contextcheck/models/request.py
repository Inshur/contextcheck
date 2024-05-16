from typing import Self

from pydantic import BaseModel

from contextcheck.models.models import TestStep


class RequestBase(BaseModel):

    @classmethod
    def from_test_step(cls, test_step: TestStep) -> Self:
        raise NotImplementedError("This method should be implemented!")
