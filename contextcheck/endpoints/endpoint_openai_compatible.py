from pydantic import model_serializer, model_validator

from contextcheck.connectors.connector_openai_compatible import ConnectorOpenAICompatible
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.response import ResponseStats


class EndpointOpenAICompatible(EndpointBase):
    connector: ConnectorOpenAICompatible = ConnectorOpenAICompatible()

    class RequestModel(EndpointBase.RequestModel):
        @model_serializer
        def serialize(self) -> dict:
            return {"role": "user", "content": self.message}

    class ResponseModel(EndpointBase.ResponseModel):
        @model_validator(mode="before")
        def from_dict(cls, data: dict) -> dict:
            data["message"] = data["choices"][0]["message"]["content"]

            # Attempt to collect stats 
            if "usage" in data and "prompt_tokens" in data["usage"] and "completion_tokens" in data["usage"] and "total_tokens" in data["usage"]:                    
                data["stats"] = ResponseStats(
                    tokens_request=data["usage"]["prompt_tokens"],
                    tokens_response=data["usage"]["completion_tokens"],
                    tokens_total=data["usage"]["total_tokens"],
                )
            return data
