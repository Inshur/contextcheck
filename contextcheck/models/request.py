from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic_core import from_json

fields_computation_map = {"eval": lambda x, context: eval(str(x), context)}


def replace_str_with_json(d: dict) -> dict:
    """Replace all strings JSON-parsable with corresponding python object."""

    if "parse_response_as_json" in d:
        for k, v in d.items():
            if isinstance(v, str) and check_beginning_bracket(v):  # Clumsy way to c
                try:
                    d[k] = from_json(v)
                except ValueError:  # Means that string is not json, leave it alone
                    pass
            elif isinstance(v, dict):
                d[k] = replace_str_with_json(v)
            else:
                continue

    return d


def check_beginning_bracket(s: str) -> bool:
    """Check if string starts with bracket."""
    try:
        return s.strip()[0] in ("{", "[")
    except IndexError:
        return False


class RequestBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    message: str | dict | None = None

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: str | dict) -> dict:
        """
        If request is a string, return it as message field.
        If request is a dict, dig deeper for string and convert it to dict if json.
        """
        return replace_str_with_json(obj) if isinstance(obj, dict) else {"message": obj}

    def build(self, context: dict | None = None) -> Self:
        """Build request based on prototype values."""

        def _search_and_replace(d: dict) -> dict:
            """Search recursively dict for computation string and replace it with function result."""
            # NOTE: Hmm, What if d = {"eval": "1 == 2", "value1": {"eval": "1 == 2"}}
            # then the first eval would make d of type bool and d[key] = ... would raise an error
            # Unless the result of an eval is not a dict then this will cause problems
            # TODO: Fix it if time allows or forbid too deep nesting i.e. one level should be ok
            for key, value in d.items():
                if key in fields_computation_map:
                    d = fields_computation_map[key](value, context)
                elif isinstance(value, dict):
                    d[key] = _search_and_replace(value)
            return d

        return self.model_validate(_search_and_replace(self.model_dump()))
