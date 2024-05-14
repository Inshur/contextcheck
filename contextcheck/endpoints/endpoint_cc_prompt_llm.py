from typing import Callable, ClassVar, Self

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.messages import MessageBase, ResponseBase, ResponseStats
from contextcheck.models.models import TestStep


class Message(MessageBase):
    prompt: str | None = None

    @classmethod
    def from_test_step(cls, test_step: TestStep) -> Self:
        return cls(prompt=test_step.message)

    def to_dict(self) -> dict:
        d = {"prompt": self.prompt}
        return d


class Response(ResponseBase):
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        message = data["answer"]
        # TODO: Get from headers
        response_stats = ResponseStats()
        return cls(message=message, stats=response_stats)


class EndpointCCPromptLLM(EndpointBase):
    kind: ClassVar[str] = "cc_prompt_llm"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._message_class = Message
        self._response_class = Response
        self.prepare_message: Callable = self._message_class.from_test_step
        self._connector: ConnectorHTTP = ConnectorHTTP(
            url=self.config.url, additional_headers=self.config.additional_headers
        )

    def send_message(self, message: Message) -> ResponseBase:
        response_dict = self._connector.send(message.to_dict())
        response = self._response_class.from_dict(response_dict)
        return response
