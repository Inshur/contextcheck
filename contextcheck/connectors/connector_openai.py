import dotenv
from openai import OpenAI
from pydantic import Field

from contextcheck.connectors.connector import ConnectorBase

dotenv.load_dotenv()


class ConnectorOpenAI(ConnectorBase):
    model: str = Field(default="gpt-4o-mini", description="OpenAI llm model used for inference")

    @property
    def _client(self) -> OpenAI:
        return OpenAI()

    def send(self, data: dict) -> dict:
        chat_completion = self._client.chat.completions.create(
            messages=[data], model=self.model  # type: ignore
        )
        return chat_completion.to_dict()
