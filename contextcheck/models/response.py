from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class ResponseStats(BaseModel):
    model_config = ConfigDict(extra="allow")
    tokens_request: int | None = None
    tokens_response: int | None = None
    tokens_total: int | None = None


error_message = """You see this error because of incorrect response parsing.
Your response's dictionary format causes validation error.
In order to avoid this error, you can `parse_response_as_json: true` either 
in your config.default_request or in the request step. Example:

config:
    endpoint_under_test:
        kind: echo
    default_request:
        parse_response_as_json: true  # Set globally for all tests in this file

steps:
  - name: test parsing as json
    request: '{"Hello": "World"}'
    parse_response_as_json: true  # Set for this test only
"""


class ResponseBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    message: str | None = None
    stats: ResponseStats = ResponseStats()

    @model_validator(mode="before")
    @classmethod
    def from_obj(cls, obj: dict) -> dict:
        if (
            obj.get("parse_response_as_json")
            and obj.get("message")
            and isinstance(obj["message"], dict)
            and obj["parse_response_as_json"] == True
        ):
            raise ValueError(error_message)
        return obj
