from typing import Annotated

from openai import BaseModel
from pydantic import AfterValidator, AnyUrl

from contextcheck.connectors.connector import ConnectorBase
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class EndpointConfig(BaseModel):
    kind: str | None = "openai"
    endpoint_url: Annotated[AnyUrl, AfterValidator(str)] | None = None
    additional_headers: dict | None = {}


class EndpointBase(BaseModel):
    _connector: ConnectorBase = ConnectorBase()
    config: EndpointConfig = EndpointConfig()

    class RequestModel(RequestBase):
        pass

    class ResponseModel(ResponseBase):
        pass

    def send_request(self, req: RequestBase) -> ResponseBase:
        req = self.RequestModel(**req.model_dump())
        with self._connector as c:
            response_dict = c.send(req.render())
            response_dict["_stats"] = c._stats
        response = self.RequestModel(**response_dict)
        return response
