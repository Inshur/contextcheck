from pydantic import model_serializer

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase

# NOTE RB: No custom ResponseModel and I suppose it might be needed, e.g. to assign message to model
# LATER


class EndpointCC(EndpointBase):
    class RequestModel(RequestBase):
        @model_serializer
        def serialize(self) -> dict:
            # include possible request fields prompt for QA, query for semantic search
            return {"prompt": self.message, "query": self.message}

    def model_post_init(self, __context) -> None:
        self.connector = ConnectorHTTP(
            url=self.config.url,
            additional_headers=self.config.additional_headers,
        )
