from pydantic import BaseModel, ConfigDict, model_validator

from contextcheck.models.response import ResponseBase


class AssertionBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        # Default assertion without keyword:
        return obj if isinstance(obj, dict) else {"eval": obj}

    def __call__(self, response: ResponseBase) -> bool:
        raise NotImplementedError


class AssertionEval(AssertionBase):
    eval: str

    def __call__(self, response: ResponseBase) -> bool:
        if self.result is None:
            self.result = bool(eval(self.eval))  # Should be bool
        return self.result
