import os

from openai import OpenAI

from contextcheck.connectors.connector import ConnectorBase


class ConnectorOpenAI(ConnectorBase):

    def __init__(self):
        self.api_key: str = os.environ.get("OPENAI_API_KEY")
        self.client: OpenAI = OpenAI(api_key=self.api_key)
        self.model: str = "gpt-3.5-turbo"

    def send(self, data: dict):
        chat_completion = self.client.chat.completions.create(
            messages=[data],
            model=self.model,
        )
        return chat_completion
