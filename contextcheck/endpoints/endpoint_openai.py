from typing import Self

from contextcheck.connectors.connector_openai import ConnectorOpenAI
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase, ResponseStats


class EndpointOpenAI(EndpointBase):
    _connector: ConnectorOpenAI = ConnectorOpenAI()

    class RequestModel(RequestBase):

        def render(self) -> dict:
            return {"role": "user", "content": self.message}

    class ResponseModel(ResponseBase):
        @classmethod
        def from_dict(cls, data: dict) -> Self:
            message = data["choices"][0]["message"]["content"]
            response_stats = ResponseStats(
                tokens_request=data["usage"]["prompt_tokens"],
                tokens_response=data["usage"]["completion_tokens"],
                tokens_total=data["usage"]["total_tokens"],
            )
            return cls(message=message, _stats=response_stats)
