from pydantic import Field, model_serializer

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase, EndpointConfig
from contextcheck.models.request import RequestBase


# TODO: Add Fields with defaults and descriptions
class EndpointCCConfig(EndpointConfig):
    top_k: int = 3
    use_ranker: bool = True
    collection_name: str = "default"
    url: str = ""  # AnyUrl type can be applied
    additional_headers: dict = {}


class EndpointCC(EndpointBase):
    config: EndpointCCConfig = Field(
        default_factory=EndpointCCConfig, description="Configuration for CC ednpoint"
    )

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
