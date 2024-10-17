import dotenv
from langchain import chat_models
from langchain_community.adapters import openai as openai_compatibile
from pydantic import Field, field_validator

from contextcheck.connectors.connector import ConnectorBase

dotenv.load_dotenv()


class ConnectorOpenAICompatible(ConnectorBase):
    model: str | None = Field(
        default=None, description="A model used for a request"
    )  # NOTE RB: None should not be allowed?
    provider: str | None = Field(
        default=None, description="A name of the provider"
    )  # NOTE RB: None should not be allowed?
    temperature: float | None = Field(default=None, description="Temperature used for the llm")
    max_tokens: int | None = Field(default=None, description="Max tokens for llm output")

    @field_validator("provider", mode="before")
    @classmethod
    def validated_provider(cls, provider: str | None) -> str | None:
        if provider is not None:
            if provider not in chat_models.__all__:
                raise ValueError(
                    f"Provider '{provider}' not found. Choose one of: {chat_models.__all__}"
                )

        return provider

    def send(self, data: dict) -> dict:

        # NOTE RB: If `model` and `provider` are allowed to be None, then describe how does it work
        kwargs = {
            "messages": [data],
            "model": self.model,
            "provider": self.provider,
        }

        if self.temperature:
            kwargs["temperature"] = self.temperature

        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        chat_completion = openai_compatibile.chat.completions.create(**kwargs)
        return dict(chat_completion)
