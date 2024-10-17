from enum import StrEnum

from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.endpoints.endpoint_cc import EndpointCC
from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.endpoints.endpoint_dummy_echo import EndpointDummyEcho
from contextcheck.endpoints.endpoint_openai import EndpointOpenAI
from contextcheck.endpoints.endpoint_openai_compatible import EndpointOpenAICompatible
from contextcheck.endpoints.endpoint_tg_chatbot import EndpointTGChatBot


class EndpointsEnum(StrEnum):
    OPENAI = "openai"
    OPENAI_COMPATIBLE = "openai_compatible"
    TG_CHATBOT = "tg_chatbot"
    ECHO = "echo"
    CC_PROMPT_LLM = "cc_prompt_llm"
    CC_SS = "cc_ss"


ENDPOINT_MAPPING = {
    EndpointsEnum.OPENAI: EndpointOpenAI,
    EndpointsEnum.OPENAI_COMPATIBLE: EndpointOpenAICompatible,
    EndpointsEnum.TG_CHATBOT: EndpointTGChatBot,
    EndpointsEnum.ECHO: EndpointDummyEcho,
    EndpointsEnum.CC_PROMPT_LLM: EndpointCC,
    EndpointsEnum.CC_SS: EndpointCC,
}


def factory(endpoint_config: EndpointConfig) -> EndpointBase:
    kind = endpoint_config.kind
    try:
        endpoint_class = endpoint_map[kind]
    except KeyError:
        raise ValueError("No endpoint for this kind of config.")

    return endpoint_class(config=endpoint_config)
