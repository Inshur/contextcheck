from contextcheck.connectors.connector import ConnectorBase


class ConnectorEcho(ConnectorBase):
    def send(self, data: dict) -> dict:
        return data
