from pydantic import BaseModel, ConfigDict

from contextcheck.connectors.connector import ConnectorBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class EndpointConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    kind: str = "openai"
    url: str = ""  # AnyUrl type can be applied
    additional_headers: dict = {}


class EndpointBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    connector: ConnectorBase = ConnectorBase()
    config: EndpointConfig = EndpointConfig()

    class RequestModel(RequestBase):
        pass

    class ResponseModel(ResponseBase):
        pass

    def send_request(self, req: RequestBase) -> ResponseBase:
        req = self.RequestModel(**req.model_dump())
        with self.connector as c:
            response_dict = c.send(req.model_dump())
        response = self.ResponseModel.model_validate(response_dict)

        # Add connector stats to response stats:
        response.stats = response.stats.model_copy(update=c.stats.model_dump())

        return response
