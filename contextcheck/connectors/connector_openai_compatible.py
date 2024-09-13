import dotenv
from langchain import chat_models
from langchain_community.adapters import openai as openai_compatibile

from contextcheck.connectors.connector import ConnectorBase

dotenv.load_dotenv()


def check_provider(provider: str) -> None:
    if provider not in chat_models.__all__:
        raise ValueError(f"Provider '{provider}' not found. Choose one of: {chat_models.__all__}")


class ConnectorOpenAICompatible(ConnectorBase):
    model: str | None = None  # NOTE RB: None should not be allowed
    provider: str | None = None  # NOTE RB: None should not be allowed
    temperature: float | None = None
    max_tokens: int | None = None

    def send(self, data: dict) -> dict:

        # NOTE RB: This should be a field_validator
        if self.provider is not None:
            check_provider(self.provider)

        args = {
            "messages": [data],
            "model": self.model,
            "provider": self.provider,
        }

        if self.temperature:
            args["temperature"] = self.temperature

        if self.max_tokens:
            args["max_tokens"] = self.max_tokens

        chat_completion = openai_compatibile.chat.completions.create(**args)
        return dict(chat_completion)
