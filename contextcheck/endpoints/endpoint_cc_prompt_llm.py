from typing import Callable, ClassVar, Self

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.models import TestStep
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase, ResponseStats


class Message(RequestBase):
    prompt: str | None = None

    @classmethod
    def from_test_step(cls, test_step: TestStep) -> Self:
        return cls(prompt=test_step.request.message)

    def to_dict(self) -> dict:
        return {"prompt": self.prompt}


class Response(ResponseBase):
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        message = data["answer"]
        # TODO: Get from headers
        response_stats = ResponseStats()
        return cls(message=message, stats=response_stats)


class EndpointCCPromptLLM(EndpointBase):
    kind: ClassVar[str] = "cc_prompt_llm"
    prepare_message: Callable = Message.from_test_step

    @property
    def _connector(self) -> ConnectorHTTP:
        return ConnectorHTTP(url=self.config.url, additional_headers=self.config.additional_headers)

    def send_message(self, message: Message) -> ResponseBase:
        response_dict = self._connector.send(message.to_dict())
        response = Response.from_dict(response_dict)
        return response
