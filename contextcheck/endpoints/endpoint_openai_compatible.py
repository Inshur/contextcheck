from pydantic import model_serializer, model_validator

from contextcheck.connectors.connector_openai_compatible import ConnectorOpenAICompatible
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase, ResponseStats


class EndpointOpenAICompatible(EndpointBase):
    connector: ConnectorOpenAICompatible = ConnectorOpenAICompatible()

    def model_post_init(self, __context) -> None:
        # NOTE RB: I kinda don't understand it tbh, especially the part with model_dump
        # NOTE RB: Why is it even there if we exclude all the fields (apart from stats)?
        self.connector = ConnectorOpenAICompatible(
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
