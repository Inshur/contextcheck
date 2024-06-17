import os

import dotenv
from openai import OpenAI

from contextcheck.connectors.connector import ConnectorBase
from contextcheck.endpoints.endpoint_config import EndpointConfig

dotenv.load_dotenv()


class ConnectorOpenAI(ConnectorBase):
    api_key: str = os.environ["OPENAI_API_KEY"]
    config: EndpointConfig = EndpointConfig()

    @property
    def _client(self) -> OpenAI:
        return OpenAI(api_key=self.api_key)

    def send(self, data: dict) -> dict:
        chat_completion = self._client.chat.completions.create(
            messages=[data], model=self.config.model  # type: ignore
        )
        return chat_completion.to_dict()
