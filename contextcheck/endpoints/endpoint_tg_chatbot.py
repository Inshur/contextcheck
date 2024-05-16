import json

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase


class EndpointTGChatBot(EndpointBase):

    class RequestModel(RequestBase):
        def render(self):
            d = super().render()
            if "asr_build" in d:
                d["asr_build"] = json.loads(d["asr_build"])
            return d

    @property
    def _connector(self) -> ConnectorHTTP:
        return ConnectorHTTP(
            url=self.config.url,
            additional_headers=self.config.additional_headers,
        )
