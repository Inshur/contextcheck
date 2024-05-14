import os

from openai import OpenAI

from contextcheck.connectors.connector import ConnectorBase


class ConnectorOpenAI(ConnectorBase):
    api_key: str = os.environ.get("OPENAI_API_KEY")
    model: str = "gpt-3.5-turbo"

    @property
    def _client(self) -> OpenAI:
        return OpenAI(api_key=self.api_key)

    def send(self, data: dict) -> dict:
        chat_completion = self._client.chat.completions.create(
            messages=[data],
            model=self.model,
        )
        return chat_completion.to_dict()
