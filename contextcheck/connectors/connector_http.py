from typing import Dict, Optional

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
        # NOTE RB: I kinda don't understand how does the `data` parameter works, as in some connectors
        # it represent message history (ConnectorOpenAI) and in here it represents every body parameter
        # NOTE RB: In some connectors params like tempereture, max_tokens etc. are parametrized in the
        # model (ConnectorOpenAICompatible), sometimes they are not given at all (ConnectorOpenAI) and
        # sometimes they could be given implicitly (ConnectorHTTP)
        # NOTE RB: Use timeout from parameters if provided
        response = requests.post(
            url=self.url,
            json=data if json else None,
            data=data if not json else None,
            params=params,
            timeout=self.timeout,
            headers=self.additional_headers,
        )
        response.raise_for_status()
        return response.json()
