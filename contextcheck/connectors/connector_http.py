import requests

from contextcheck.connectors.connector import ConnectorBase


class ConnectorHTTP(ConnectorBase):
    additional_headers: dict = {}
    url: str
    method: str = "POST"
    timeout: int = 30

    def send(
        self, data: dict, json: bool = True, params: dict | None = None, timeout: int | None = None
    ) -> dict:
        response = requests.request(
            method=self.method,
            url=self.url,
            json=data if json else None,
            data=data if not json else None,
            params=params,
            timeout=timeout or self.timeout,
            headers=self.additional_headers,
        )
        response.raise_for_status()
        return response.json()
