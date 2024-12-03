import dotenv
from langchain.chat_models import ChatVertexAI
from pydantic import Field, field_validator
import google.cloud.aiplatform as aiplatform

from contextcheck.connectors.connector import ConnectorBase

dotenv.load_dotenv()


class ConnectorVertexAICompatible(ConnectorBase):
    model: str = Field(default="gemini-pro", description="A model used for a request")
    provider: str = Field(default="ChatVertexAI", description="A name of the provider")
    temperature: float | None = Field(default=None, description="Temperature used for the llm")
    max_tokens: int | None = Field(default=None, description="Max tokens for llm output")
    project: str | None = Field(default=None, description="Google Cloud project ID")
    location: str = Field(default="us-central1", description="Google Cloud region")

    def __init__(self, **data):
        super().__init__(**data)
        # Initialize Vertex AI with the project and location
        aiplatform.init(project=self.project, location=self.location)

    @field_validator("provider", mode="before")
    @classmethod
    def validated_provider(cls, provider: str) -> str:
        if provider not in ["ChatVertexAI"]:
            raise ValueError(f"Provider must be 'ChatVertexAI'")
        return provider

    def send(self, data: dict) -> dict:
        kwargs = {
            "model_name": self.model,
            "temperature": self.temperature if self.temperature is not None else 0,
            "max_output_tokens": self.max_tokens,
            "project": self.project,
            "location": self.location,
        }

        chat_model = ChatVertexAI(**kwargs)
        messages = [{"role": "user", "content": data["message"]}]
        response = chat_model.invoke(messages)
        
        return {
            "choices": [{"message": {"content": response.content}}],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }