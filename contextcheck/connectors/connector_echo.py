from contextcheck.connectors.connector import ConnectorBase


class ConnectorEcho(ConnectorBase):
    """Sends the same data as received."""

    def send(self, data: dict) -> dict:
        return data
