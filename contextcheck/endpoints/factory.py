from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.endpoints.endpoint_cc import EndpointCC
from contextcheck.endpoints.endpoint_config import EndpointConfig, EndpointsEnum
from contextcheck.endpoints.endpoint_dummy_echo import EndpointDummyEcho
from contextcheck.endpoints.endpoint_openai_compatible import EndpointOpenAICompatible
from contextcheck.endpoints.endpoint_tg_chatbot import EndpointTGChatBot
from contextcheck.endpoints.endpoint_vertexai_compatible import EndpointVertexAICompatible

ENDPOINT_MAPPING: dict[EndpointsEnum, EndpointBase] = {
    EndpointsEnum.OPENAI: EndpointOpenAICompatible,
    EndpointsEnum.OPENAI_COMPATIBLE: EndpointOpenAICompatible,
    EndpointsEnum.VERTEXAI_COMPATIBLE: EndpointVertexAICompatible,
    EndpointsEnum.TG_CHATBOT: EndpointTGChatBot,
    EndpointsEnum.ECHO: EndpointDummyEcho,
    EndpointsEnum.CC_PROMPT_LLM: EndpointCC,
    EndpointsEnum.CC_SS: EndpointCC,
}


def factory(endpoint_config: EndpointConfig) -> EndpointBase:
    kind = endpoint_config.kind
    try:
        endpoint_class = ENDPOINT_MAPPING[kind]
    except KeyError:
        raise ValueError("No endpoint for this kind of config.")

    return endpoint_class(config=endpoint_config.model_dump())
