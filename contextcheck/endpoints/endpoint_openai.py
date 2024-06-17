from pydantic import model_serializer, model_validator

from contextcheck.connectors.connector_openai import ConnectorOpenAI
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.response import ResponseStats
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class EndpointOpenAI(EndpointBase):
    connector: ConnectorOpenAI = ConnectorOpenAI()

    class RequestModel(RequestBase):
        @model_serializer
        def serialize(self) -> dict:
            return {"role": "user", "content": self.message}

    class ResponseModel(ResponseBase):
        @model_validator(mode="before")
        def from_dict(cls, data: dict) -> dict:
            data["message"] = data["choices"][0]["message"]["content"]
            data["stats"] = ResponseStats(
                tokens_request=data["usage"]["prompt_tokens"],
                tokens_response=data["usage"]["completion_tokens"],
                tokens_total=data["usage"]["total_tokens"],
            )
            return data
