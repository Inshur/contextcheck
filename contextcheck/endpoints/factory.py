from contextcheck.endpoints.endpoint import EndpointBase, EndpointConfig
from contextcheck.endpoints.endpoint_cc_prompt_llm import EndpointCCPromptLLM
from contextcheck.endpoints.endpoint_dummy_echo import EndpointDummyEcho
from contextcheck.endpoints.endpoint_openai import EndpointOpenAI
from contextcheck.endpoints.endpoint_tg_chatbot import EndpointTGChatBot

endpoint_map = {
    "openai": EndpointOpenAI,
    "cc_prompt_llm": EndpointCCPromptLLM,
    "tg_chatbot": EndpointTGChatBot,
    "echo": EndpointDummyEcho,
}


def factory(endpoint_config: EndpointConfig) -> EndpointBase:
    kind = endpoint_config.kind
    try:
        endpoint_class = endpoint_map[kind]
    except KeyError:
        raise ValueError("No endpoint for this kind of config.")

    return endpoint_class(config=endpoint_config)
