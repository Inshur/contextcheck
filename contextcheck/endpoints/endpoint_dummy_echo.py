from contextcheck.connectors.connector_echo import ConnectorEcho
from contextcheck.endpoints.endpoint import EndpointBase


class EndpointDummyEcho(EndpointBase):
    connector: ConnectorEcho = ConnectorEcho()
