from typing import Callable, ClassVar, Self

from contextcheck.connectors.connector_openai import ConnectorOpenAI
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.messages import MessageBase, ResponseBase, ResponseStats
from contextcheck.models.models import TestStep


class Message(MessageBase):
    message_system: str | None = None
    message_user: str | None = None

    @classmethod
    def from_test_step(cls, test_step: TestStep) -> Self:
        return cls(message_user=test_step.message)

    def to_dict(self) -> dict:
        return {"role": "user", "content": self.message_user}


class Response(ResponseBase):
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
    kind: ClassVar[str] = "openai"
    prepare_message: Callable = Message.from_test_step
    _connector: ConnectorOpenAI = ConnectorOpenAI()

    def send_message(self, message: Message) -> ResponseBase:
        response_dict = self._connector.send(message.to_dict())
        response = Response.from_dict(response_dict)
        return response
