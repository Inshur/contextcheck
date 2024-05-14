from typing import Callable, Self

from contextcheck.connectors.connector import ConnectorBase
from contextcheck.connectors.connector_openai import ConnectorOpenAI
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.messages import MessageBase
from contextcheck.models.models import TestStep


class MessageOpenAI(MessageBase):
    message_system: str | None = None
    message_user: str | None = None

    @classmethod
    def from_test_step(cls, test_step: TestStep) -> Self:
        return cls(message_user=test_step.message)

    def to_dict(self):
        d = {"role": "user", "content": self.message_user}
        return d


class EndpointOpenAI(EndpointBase):
    def __init__(self) -> None:
        super().__init__()
        self._message_class = MessageOpenAI
        self.prepare_message: Callable = self._message_class.from_test_step
        self._connector: ConnectorOpenAI = ConnectorOpenAI()

    def send_message(self, message: MessageOpenAI):
        return self._connector.send(message.to_dict())
