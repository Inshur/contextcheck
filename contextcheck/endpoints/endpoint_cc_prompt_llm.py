from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase


class EndpointCCPromptLLM(EndpointBase):

    class RequestModel(RequestBase):

        def render(self) -> dict:
            return {"prompt": self.message}

    @property
    def _connector(self) -> ConnectorHTTP:
        return ConnectorHTTP(
            url=self.config.url,
            additional_headers=self.config.additional_headers,
        )
