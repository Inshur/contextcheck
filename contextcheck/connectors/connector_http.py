from typing import Self

from contextcheck.connectors.connector import ConnectorBase
from contextcheck.models.messages import MessagePayloadBase


class ConnectorHTTP(ConnectorBase):
    additional_headers: dict = {}

    def send_message(self, message_payload: MessagePayloadBase): ...
