from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.endpoints.endpoint_dummy_echo import EndpointDummyEcho
from contextcheck.endpoints.endpoint_openai import EndpointOpenAI
from contextcheck.endpoints.endpoint_openai_compatible import EndpointOpenAICompatible
from contextcheck.endpoints.endpoint_tg_chatbot import EndpointTGChatBot
from contextcheck.endpoints.endpoint_cc import EndpointCC

endpoint_map = {
    "openai": EndpointOpenAI,
    "openai_compatible": EndpointOpenAICompatible,
    "tg_chatbot": EndpointTGChatBot,
    "echo": EndpointDummyEcho,
    "cc_prompt_llm": EndpointCC,
    "cc_ss": EndpointCC,

}


def factory(endpoint_config: EndpointConfig) -> EndpointBase:
    kind = endpoint_config.kind
    try:
        endpoint_class = endpoint_map[kind]
    except KeyError:
        raise ValueError("No endpoint for this kind of config.")

    return endpoint_class(config=endpoint_config)
