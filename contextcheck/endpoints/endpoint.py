from typing import Annotated, ClassVar, Literal

from openai import BaseModel
from pydantic import AfterValidator, AnyUrl

from contextcheck.connectors.connector import ConnectorBase


class EndpointConfig(BaseModel):
    kind: str | None = "openai"
    endpoint_url: Annotated[AnyUrl, AfterValidator(str)] | None = None
    additional_headers: dict | None = {}
    request_format: str | None = None


class EndpointBase(BaseModel):
    kind: ClassVar[str] = "base"
    # connector: ConnectorBase
    config: EndpointConfig = EndpointConfig()


def factory(endpoint_config: EndpointConfig) -> EndpointBase:
    kind = endpoint_config.kind
    try:
        ep_cls = next(cls for cls in EndpointBase.__subclasses__() if cls.kind == kind)
    except StopIteration:
        raise ValueError("No endpoint for this kind of config.")
    return ep_cls(config=endpoint_config)
