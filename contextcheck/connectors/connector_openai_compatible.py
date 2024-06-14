import dotenv
from langchain import chat_models
from langchain_community.adapters import openai as openai_compatibile

from contextcheck.connectors.connector import ConnectorBase


dotenv.load_dotenv()


def check_provider(provider: str) -> None:
    if provider not in chat_models.__all__:
        raise ValueError(f"Provider '{provider}' not found. Choose one of: {chat_models.__all__}")


class ConnectorOpenAICompatible(ConnectorBase):

    def send(self, data: dict) -> dict:

        if self.config.provider is not None:
            check_provider(self.config.provider)

        args = {
            "messages": [data],
            "model": self.config.model,
            "provider": self.config.provider,
        }

        if self.config.temperature:
            args["temperature"] = self.config.temperature

        if self.config.max_tokens:
            args["max_tokens"] = self.config.max_tokens

        chat_completion = openai_compatibile.chat.completions.create(**args)
        return dict(chat_completion)
