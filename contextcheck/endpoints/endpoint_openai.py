from typing import Callable, Self

from contextcheck.connectors.connector import ConnectorBase
from contextcheck.connectors.connector_openai import ConnectorOpenAI
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.messages import MessageBase, ResponseBase, ResponseStats
from contextcheck.models.models import TestStep


class MessageOpenAI(MessageBase):
    message_system: str | None = None
    message_user: str | None = None

    @classmethod
    def from_test_step(cls, test_step: TestStep) -> Self:
        return cls(message_user=test_step.message)

    def to_dict(self) -> dict:
        d = {"role": "user", "content": self.message_user}
        return d


class ResponseOpenAI(ResponseBase):
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        message = data["choices"][0]["message"]["content"]
        response_stats = ResponseStats(
            tokens_message=data["usage"]["prompt_tokens"],
            tokens_response=data["usage"]["completion_tokens"],
            tokens_total=data["usage"]["total_tokens"],
        )
        return cls(message=message, stats=response_stats)


class EndpointOpenAI(EndpointBase):
    def __init__(self) -> None:
        super().__init__()
        self._message_class = MessageOpenAI
        self._response_class = ResponseOpenAI
        self.prepare_message: Callable = self._message_class.from_test_step
        self._connector: ConnectorOpenAI = ConnectorOpenAI()

    def send_message(self, message: MessageOpenAI) -> ResponseBase:
        response_dict = self._connector.send(message.to_dict())
        response = self._response_class.from_dict(response_dict)
        return response
