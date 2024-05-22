from pydantic import BaseModel, ConfigDict, model_validator

from contextcheck.models.response import ResponseBase


class AssertionBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict | str) -> dict:
        return obj if type(obj) is dict else {"eval": obj}


class AssertionEval(AssertionBase):
    eval: str

    def check(self, response: ResponseBase) -> bool:
        self.result = bool(eval(self.eval))  # Should be bool
        return self.result
