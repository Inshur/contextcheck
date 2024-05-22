from pydantic import BaseModel, ConfigDict, model_validator


class RequestBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    message: str | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: str | dict) -> dict:
        return obj if type(obj) is dict else {"message": obj}

    # def render(self) -> dict:
    #     """Render request dict from the model"""
    #     return self.model_dump()
    #     # raise NotImplementedError("Request render method not implemented")
