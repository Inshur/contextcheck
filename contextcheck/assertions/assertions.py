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
            try:
                result = eval(self.eval)
            except NameError:
                raise NameError(f"Given eval `{self.eval}` uses non-existent name.")
            if not isinstance(result, bool):
                raise ValueError(f"Given eval `{self.eval}` does not evaluate to bool.")
            self.result = result
        return self.result
