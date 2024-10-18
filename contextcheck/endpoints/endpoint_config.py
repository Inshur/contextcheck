from pydantic import BaseModel, ConfigDict
from enum import StrEnum


class EndpointsEnum(StrEnum):
    OPENAI = "openai"
    OPENAI_COMPATIBLE = "openai_compatible"
    TG_CHATBOT = "tg_chatbot"
    ECHO = "echo"
    CC_PROMPT_LLM = "cc_prompt_llm"
    CC_SS = "cc_ss"


# NOTE RB: Imo, we should think how to refactor this as not every endpoint need those params
# and some new endpoints/connectors might need other values
# NOTE: Not every Endpoint needs to use custom EndpointConfig
class EndpointConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    kind: EndpointsEnum = EndpointsEnum.OPENAI
    model: str | None = "gpt-4o-mini"
    temperature: float | None = None
    max_tokens: int | None = None
