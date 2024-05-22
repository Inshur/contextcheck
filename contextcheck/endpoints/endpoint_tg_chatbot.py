import json

from pydantic import field_validator

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase


class EndpointTGChatBot(EndpointBase):

    class RequestModel(RequestBase):
        asr_build: dict | None = None

        @field_validator("asr_build", mode="before")
        @classmethod
        def asr_converstion(cls, obj: str | dict) -> dict:
            if type(obj) is str:
                return json.loads(obj)
            elif type(obj) is dict:
                return obj
            else:
                raise ValueError(
                    "ASR provided in a wrong format (should be str or dict)"
                )

    @property
    def _connector(self) -> ConnectorHTTP:
        return ConnectorHTTP(
            url=self.config.url,
            additional_headers=self.config.additional_headers,
        )
