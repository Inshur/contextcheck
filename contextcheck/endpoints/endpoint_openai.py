from pydantic import model_serializer, model_validator

from contextcheck.connectors.connector_openai import ConnectorOpenAI
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase, ResponseStats


class EndpointOpenAI(EndpointBase):
    connector: ConnectorOpenAI = ConnectorOpenAI()

    def model_post_init(self, __context) -> None:
        # NOTE RB: What exactly is given by `self.connector.model_dump`, as it seems that it only
        # should have `model` (which is dropped), `api_key` (which is given by default) and `stats`
        # which I suppose is not given, but simply uses default (unless I'm wrong)
        self.connector = ConnectorOpenAI(
            model=self.config.model, **self.connector.model_dump(exclude={"model"})
        )

    class RequestModel(RequestBase):
        # NOTE RB: This model does not allow sending configurations to openai, but simply a message
        @model_serializer
        def serialize(self) -> dict:
            return {"role": "user", "content": self.message}

    class ResponseModel(ResponseBase):
        @model_validator(mode="before")
        @classmethod
        def from_dict(cls, data: dict) -> dict:
            # NOTE RB: I'd create a new dict to remove the output from a particular model
            # or at least give it under a special name like _model_output
            # NOTE RB: Or explicitly state which values are allowed by the model
            data["message"] = data["choices"][0]["message"]["content"]
            data["stats"] = ResponseStats(
                tokens_request=data["usage"]["prompt_tokens"],
                tokens_response=data["usage"]["completion_tokens"],
                tokens_total=data["usage"]["total_tokens"],
            )
            return data
