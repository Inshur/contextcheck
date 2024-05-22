import requests

from contextcheck.connectors.connector import ConnectorBase


class ConnectorHTTP(ConnectorBase):
    additional_headers: dict = {}
    url: str
    method: str = "POST"
    timeout: int = 30

    def send(
        self, data: dict, params: dict | None = None, timeout: int | None = None
    ) -> dict:
        params = params or {}
        response = requests.post(
            url=self.url,
            json=data,
            params=params,
            timeout=timeout or self.timeout,
            headers=self.additional_headers,
        )
        response.raise_for_status()
        return response.json()
