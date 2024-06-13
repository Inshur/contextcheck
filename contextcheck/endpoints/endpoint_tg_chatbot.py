from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase


class EndpointTGChatBot(EndpointBase):

    def model_post_init(self, __context) -> None:
        self.connector = ConnectorHTTP(
            url=self.config.url,
            additional_headers=self.config.additional_headers,
        )
