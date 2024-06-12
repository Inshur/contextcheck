from pydantic import Field, model_serializer

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase


class EndpointOllama(EndpointBase):
    class RequestModel(EndpointBase.RequestModel):
        @model_serializer
        def serialize(self) -> dict:
            return {
                "prompt": self.message,
                "stream": False,
                "model": self.config.model,  # type: ignore
            }

    class ResponseModel(EndpointBase.ResponseModel):
        # Ollama return message in the `response` field
        message: str = Field(default=None, alias="response")

    def model_post_init(self, __context) -> None:
        self.config.url = (
            "http://127.0.0.1:11434/api/generate"
            if not self.config.url
            else self.config.url
        )

        self.connector = ConnectorHTTP(
            url=self.config.url,
            additional_headers=self.config.additional_headers,
        )
