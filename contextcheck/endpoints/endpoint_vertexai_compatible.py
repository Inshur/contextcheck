from pydantic import Field, model_serializer, model_validator

from contextcheck.connectors.connector_vertexai_compatible import ConnectorVertexAICompatible
from contextcheck.endpoints.endpoint import EndpointBase, EndpointConfig
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase, ResponseStats


class EndpointVertexAICompatibleConfig(EndpointConfig):
    provider: str = "ChatVertexAI"


class EndpointVertexAICompatible(EndpointBase):
    config: EndpointVertexAICompatibleConfig = Field(
        default_factory=EndpointVertexAICompatibleConfig,
        description="Configuration for endpoints compatible with VertexAI through langchain",
    )
    connector: ConnectorVertexAICompatible = ConnectorVertexAICompatible()

    def model_post_init(self, __context) -> None:
        self.connector = ConnectorVertexAICompatible(
            model=self.config.model,
            provider=self.config.provider,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **self.connector.model_dump(exclude={"model", "provider", "temperature", "max_tokens"})
        )

    class RequestModel(RequestBase):
        @model_serializer
        def serialize(self) -> dict:
            return {"role": "user", "content": self.message}

    class ResponseModel(ResponseBase):
        @model_validator(mode="before")
        @classmethod
        def from_dict(cls, data: dict) -> dict:
            data["message"] = data["choices"][0]["message"]["content"]

            # Attempt to collect stats
            if (
                "usage" in data
                and "prompt_tokens" in data["usage"]
                and "completion_tokens" in data["usage"]
                and "total_tokens" in data["usage"]
            ):
                data["stats"] = ResponseStats(
                    tokens_request=data["usage"]["prompt_tokens"],
                    tokens_response=data["usage"]["completion_tokens"],
                    tokens_total=data["usage"]["total_tokens"],
                )
            return data 