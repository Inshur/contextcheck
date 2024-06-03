from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

fields_computation_map = {"eval": lambda x, context: eval(str(x), context)}


class RequestBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    message: str | dict | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: str | dict) -> dict:
        return obj if isinstance(obj, dict) else {"message": obj}

    def build(self, context: dict | None = None) -> Self:
        """Build request based on prototype values."""

        def _search_and_replace(d: dict) -> dict:
            """Search recursively dict for computation string and replace it with function result."""
            for key, value in d.items():
                if key in fields_computation_map:
                    d = fields_computation_map[key](value, context)
                elif isinstance(value, dict):
                    d[key] = _search_and_replace(value)
            return d

        return self.model_validate(_search_and_replace(self.model_dump()))
